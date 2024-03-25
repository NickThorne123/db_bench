"""
Initial version by Nick Thorne, Rockstone Data Ltd. January 2024.
"""
from dash import Dash, dcc, html, Input, Output, State, callback
import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.express as px
import pandas as pd
from datetime import date, datetime as dt
from clickhouse_driver import Client
import time
from dotenv import load_dotenv
import os

load_dotenv()
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/

CH_HOST=os.getenv('CH_HOST')
CH_PORT=os.getenv('CH_PORT')
CH_PASSWORD=os.getenv('CH_PASSWORD')
CH_USER=os.getenv('CH_USER')
CH_DBNAME=os.getenv('CH_DBNAME')

def get_ch_client():
    """
    Create a Clickhouse DB client object (aka connection)
    """
    client = Client(host="localhost", port=9001, settings={'use_numpy': True}, user="chuser", password="chuser_pwd")
    return client

app = Dash(__name__)

# Create the app layout
app.layout = html.Div([
    dbc.Row(html.Div("""This is a demo of how we can visalise very large time series data sets using a column orientated database. """)),
    dbc.Row(html.Strong("""Drag the X axes to increase/decrease/pan the date ranges. Note the resulting query durations.""")),
    dbc.Row(html.Div("""The top chart plots a raw time series value, ie with no downsampling (with a result count limit set in [A]). """)),
    dbc.Row(html.Div("""The lower chart is identical except that the time series values are downsampled by the database to the number entered in input [B].
             """)),
    dbc.Row(html.Div([html.Span("""This is a live demo. The release tech stack is docker container running a Flask Plotly Dash app. The plots are Plotly Express Line plots. """),
                     html.Span("""There are two more containers running ClickhouseDB. """),html.Br(),
                     html.Span("""The downsampling query uses the Clickhouse """),
                    dcc.Link('largestTriangleThreeBuckets', href="https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference/largestTriangleThreeBuckets", target='_blank' ),
                    html.Span(" utility. "), html.Span(" ", id='table-len')])
             ),
    html.Br(),
    dbc.Row([dbc.Col(html.Div('[A] Limit for raw rows (top chart), max 10,000'), width=6),
             dbc.Col([dcc.Input(id='max-nonds', type='number', value=5000, debounce=True)], width = 2)
             ]),
    dbc.Row([dbc.Col(html.Div('[B] Number of points to downsample to (lower chart), max 5000'), width=6),
             dbc.Col([dcc.Input(id='std-window', type='number', value=1000, debounce=True)], width = 2),
             dbc.Col(' ', width=6)]),
   
    html.Div( style={'display': 'none'}, id='data-in'), # for callbacks with no input needed
    dcc.Graph(id='scatter-plot'),
    dcc.Graph(id='agg-scatter-plot')
])

# Add various callbacks
@app.callback(
    [Output('scatter-plot', 'figure'),
     Output('agg-scatter-plot', 'figure'),
     Output('table-len', 'children')],
    [Input('std-window', 'value'),
     Input('max-nonds', 'value'),
     Input('agg-scatter-plot','relayoutData'),
     Input('scatter-plot','relayoutData')]
    # prevent_initial_call=True
)
def update_output( std_window, max_nonds, agg_relayout, relayout):
    """
    Create the chart when inputs are changed
    """

    # self generated data range
    start_date_str = '2021-01-01 00:00:00'
    to_date_str = '2021-01-03 00:00:00'

    # Example of relayout data
    # 'xaxis.range[0]':'2023-09-14 07:40:20.0781'
    # 'xaxis.range[1]': '2023-09-14 08:40:01.0781'
    
    chosen_relayout = None

    triggered_list = dash.callback_context.triggered


    if len(triggered_list) > 0:
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if 'agg-scatter-plot' in changed_id:
            if agg_relayout is not None:
                if 'xaxis.range[0]' in agg_relayout:
                    chosen_relayout = agg_relayout
        elif 'scatter-plot' in changed_id:
            if relayout is not None:
                if 'xaxis.range[0]' in relayout:
                    chosen_relayout = relayout

    if chosen_relayout is not None: 
       print(f"agg-plot dates = {chosen_relayout['xaxis.range[0]']} and {chosen_relayout['xaxis.range[1]']}")
       start_date_str = format_time(chosen_relayout['xaxis.range[0]'])
       to_date_str = format_time(chosen_relayout['xaxis.range[1]'])
    # print(f'processed dates = {start_date_str} and {to_date_str}')

    # Limit number of downsampleds
    if std_window > 5000:
        std_window = 5000
    elif std_window < 5:
        std_window = 5
    # Limit number of raws
    if max_nonds > 10000:
        max_nonds = 10000
    elif max_nonds < 5:
        max_nonds = 5

    client = get_ch_client()

    try:
        fig = html.Br()
        # Get row count
        query =  f""" SELECT count(*) from ts_db.demo_ts  """
        total_rows = client.execute(query, settings={'use_numpy': True})[0][0]

        query =  f""" SELECT count(*) from ts_db.demo_ts WHERE cdatetime BETWEEN toDateTime('{start_date_str}') AND toDateTime('{to_date_str}') """
        res_count = client.execute(query, settings={'use_numpy': True})[0][0]

        raw_limit = max_nonds
        query =  f""" SELECT cdatetime, ts_values from ts_db.demo_ts 
                    WHERE cdatetime BETWEEN toDateTime('{start_date_str}') AND toDateTime('{to_date_str}')
                    ORDER BY cdatetime DESC LIMIT {raw_limit} """
        start_t = time.time()
        res_list = client.execute(query, settings={'use_numpy': True})
        
        df = pd.DataFrame(res_list, columns =['cdatetime','ts_values'])
        fig_row_count = df.shape[0]
        elapsed = f"query time:{(time.time() - start_t):0.2f}s" 
        fig = px.line(df, x='cdatetime', y='ts_values') 
        fig.update_layout(title_text = f"Raw Chart of {fig_row_count} samples, limited to {raw_limit} {elapsed} ", title_x=0.5, xaxis_title='Date and Time', yaxis_title = 'Raw Value')
        fig.update_xaxes(range=[start_date_str, to_date_str]) # Don't let chart autoscale sa loses impact of how few samples we're pulling compared to downsampled

        # get the downsampled values
        downsample_query = f""" from ts_db.demo_ts select untuple(arrayJoin(largestTriangleThreeBuckets({std_window})(cdatetime, ts_values )))
                    where toDateTime(cdatetime) >= toDateTime('{start_date_str}') and toDateTime(cdatetime) <= toDateTime('{to_date_str}') """
        start_t = time.time()
        res_list_agg = client.execute(downsample_query, settings={'use_numpy': True})
        elapsed = time.time() - start_t
        df_agg = pd.DataFrame(res_list_agg, columns =['cdatetime','ts_values'])
        fig_agg_row_count = df_agg.shape[0]
        fig_agg = px.line(df_agg, x='cdatetime', y='ts_values') 
        fig_agg.update_layout(title_text = f"Downsampled Chart ({fig_agg_row_count}/{std_window} of {res_count:,} rows) query time:{elapsed:0.2f}s", title_x=0.5,
                                xaxis_title='Date and Time', yaxis_title = 'Downsampled Value')
        return [fig, fig_agg, f"The table has {total_rows:,} rows."]
        
    except Exception as a:
        print(f'update_output error {a}')
    
    
    if client is not None:
        client.disconnect()

    
#    return [fig, fig_agg, f"The table has {total_rows:,} rows."]


def format_time(input_time):
    """
    Handle Dash time foibles
    """
    try:
        parsed_time = dt.strptime(input_time, '%Y-%m-%d')
        return parsed_time.strftime('%Y-%m-%d 00:00:00')
    except ValueError as e:
        # print(f'dt parse err 1 {e}')
        pass

    try:
        parsed_time = dt.strptime(input_time, '%Y-%m-%d %H:%M:%S.%f')
        return parsed_time.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        # print(f'dt parse err 1 {e}')
        pass

    try:
        parsed_time = dt.strptime(input_time, '%Y-%m-%d %H:%M')
        return parsed_time.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        # print(f'dt parse err 2 {e}') 
        pass   
    
    parsed_time = dt.strptime(input_time, '%Y-%m-%d %H:%M:%S')
    
    return parsed_time.strftime('%Y-%m-%d %H:%M:%S')

UNITS =['datetime', 'secs', 'mins', 'hours', 'dayofweek', 'weeknum', 'monthnum', 'yearnum']

if __name__ == '__main__':
    app.run(debug=True, port = 8077)


# Useful code to generate demo_ts, also see README.md
"""
CREATE TABLE demo_ts 
ENGINE = MergeTree
ORDER BY tuple()
AS
SELECT toDateTime(arrayJoin(range(toUInt32(toDateTime('2021-01-01 00:00:00')), toUInt32(toDateTime('2021-01-01 00:10:00')), 1) )) as cdatetime,
       toSecond(toDateTime(arrayJoin(range(toUInt32(toDateTime('2021-01-01 00:00:00')), toUInt32(toDateTime('2021-01-01 00:10:00')), 1) ))) +
       toMinute(toDateTime(arrayJoin(range(toUInt32(toDateTime('2021-01-01 00:00:00')), toUInt32(toDateTime('2021-01-01 00:10:00')), 1) ))) +
       2 * toHour(toDateTime(arrayJoin(range(toUInt32(toDateTime('2021-01-01 00:00:00')), toUInt32(toDateTime('2021-01-01 00:10:00')), 1) ))) +
       5 * toDayOfWeek(toDateTime(arrayJoin(range(toUInt32(toDateTime('2021-01-01 00:00:00')), toUInt32(toDateTime('2021-01-01 00:10:00')), 1) ))) +
       8 * toWeek(toDateTime(arrayJoin(range(toUInt32(toDateTime('2021-01-01 00:00:00')), toUInt32(toDateTime('2021-01-01 00:10:00')), 1) ))) +
       12 * toMonth(toDateTime(arrayJoin(range(toUInt32(toDateTime('2021-01-01 00:00:00')), toUInt32(toDateTime('2021-01-01 00:10:00')), 1) ))) +
       20 * (toYear(toDateTime(arrayJoin(range(toUInt32(toDateTime('2021-01-01 00:00:00')), toUInt32(toDateTime('2021-01-01 00:10:00')), 1) )))-2021) as ts_values

"""