from datetime import date, datetime as dt
from dotenv import load_dotenv
from clickhouse_driver import Client
import streamlit as st
import plotly.express as px
import datetime
import pandas as pd
import time
import numpy
import os

load_dotenv()

CH_HOST=os.getenv('CH_HOST')
CH_PORT=os.getenv('CH_PORT')
CH_PASSWORD=os.getenv('CH_PASSWORD')
CH_USER=os.getenv('CH_USER')
CH_DBNAME=os.getenv('CH_DBNAME')

st.set_page_config(page_title="DB Benchmark")
st.markdown("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True) #Shows radio buttons in a row. Streamlit default is vertical list

def get_ch_client():
    """Create a Clickhouse DB client object (aka connection)"""
    client = Client(host="localhost", port=9001, settings={'use_numpy': True}, user="chuser", password="chuser_pwd") #TODO shouldn't be hard coded
    return client


def submit_clicked_clickhouse(total_elapsed_time_clickhouse_downsampled, total_elapsed_time_clickhouse_raw, downsampling_on_off, clickhouse_out_raw_title, clickhouse_out,
                               clickhouse_out_downsampled_title, clickhouse_out_downsampled, start_date_clickhouse, start_time_clickhouse, end_date_clickhouse, end_time_clickhouse, downsampling_value):
    """Performs the logic to get the data from the clickhouse DB and outputs it onto streamlit when submit is clicked"""
    client = get_ch_client()

    #clickhouse_start_datetime = datetime.datetime.combine(start_date_clickhouse, start_time_clickhouse)
    #clickhouse_end_datetime = datetime.datetime.combine(end_date_clickhouse, end_time_clickhouse)

    try:
        #Get row count
        total_rows_query =  f""" SELECT count(*) from ts_db.demo_ts  """
        total_rows = client.execute(total_rows_query, settings={'use_numpy': True})[0][0]

        res_count_query =  f""" SELECT count(*) from ts_db.demo_ts WHERE cdatetime BETWEEN toDateTime('{start_date_clickhouse}') AND toDateTime('{end_date_clickhouse}') """
        res_count = client.execute(res_count_query, settings={'use_numpy': True})[0][0]

        res_list_query =  f""" SELECT cdatetime, ts_values from ts_db.demo_ts 
                    WHERE cdatetime BETWEEN toDateTime('{start_date_clickhouse}') AND toDateTime('{end_date_clickhouse}')
                    ORDER BY cdatetime DESC LIMIT 10000 """

        res_list = client.execute(res_list_query, settings={'use_numpy': True})

        clickhouse_out_raw_title.write(f"Raw Data Chart of limited 10000 samples - {total_rows:,} Total Rows")
        data_process_start_time_raw = time.time() #Gets the start time before the data is processed
        
        df = pd.DataFrame(res_list, columns =['cdatetime','ts_values'])
        fig = px.line(df, x='cdatetime', y='ts_values')
        fig.update_layout(xaxis_title='Date and Time', yaxis_title = 'Raw Value')
        fig.update_xaxes(range=[start_date_clickhouse, end_date_clickhouse]) # Don't let chart autoscale sa loses impact of how few samples we're pulling compared to downsampled
        clickhouse_out.plotly_chart(fig) #Plots a Plotly chart

        data_process_end_time_raw = time.time() #Gets the end time after data processing is complete
        total_elapsed_time_clickhouse_raw.text(f"Raw Samples Execution time: {round(data_process_end_time_raw - data_process_start_time_raw, 3)} seconds") #Shows the elapsed time to 3dp above the charts

        if downsampling_on_off: #If the downsampling toggle is selected and True #TODO SORT OUT PROPERLY!!! - Mate it to the radio buttons and downsampling number input
            data_process_start_time_downsampled = time.time() #Gets the start time before the data is processed

            #Shows downsampled values
            downsample_query = f""" from ts_db.demo_ts select untuple(arrayJoin(largestTriangleThreeBuckets({downsampling_value})(cdatetime, ts_values )))
                        where toDateTime(cdatetime) >= toDateTime('{start_date_clickhouse}') and toDateTime(cdatetime) <= toDateTime('{end_date_clickhouse}') """
            res_list_agg = client.execute(downsample_query, settings={'use_numpy': True})
            df_agg = pd.DataFrame(res_list_agg, columns =['cdatetime','ts_values'])
            fig_agg_row_count = df_agg.shape[0]
            fig_agg = px.line(df_agg, x='cdatetime', y='ts_values')
            fig_agg.update_layout(xaxis_title='Date and Time', yaxis_title = 'Downsampled Value')
            clickhouse_out_downsampled_title.write(f"Downsampled Data Chart ({fig_agg_row_count}/{downsampling_value} of {res_count:,} rows)")

            clickhouse_out_downsampled.plotly_chart(fig_agg) #Plots a Plotly chart
            data_process_end_time_downsampled = time.time() #Gets the start time before the data is processed
            total_elapsed_time_clickhouse_downsampled.text(f"Downsampled Execution time: {round(data_process_end_time_downsampled - data_process_start_time_downsampled, 3)} seconds") #Shows the elapsed time to 3dp above the charts
    except Exception as a:
        print(f'update_output error {a}')


def clickhouse_data_benchmarking_setup():
    """Displays the layout of the clickhouse widgets in streamlit"""

    st.subheader("clickhouse")

    start_time_date_col, end_time_date_col = st.columns([1, 1]) #Creates columns for the start and end date / time pickers
    with start_time_date_col:
        start_date_clickhouse = st.date_input("Data Start Date:", datetime.date(2021, 1, 1), key="start_date_clickhouse")
        start_time_clickhouse = st.time_input("Data Start Time:", key="start_time_clickhouse")
    with end_time_date_col:
        end_date_clickhouse = st.date_input("Data End Date:", datetime.date(2022, 1, 2), key="end_date_clickhouse")
        end_time_clickhouse = st.time_input("Data End Time:", key="end_time_clickhouse")

    st.write("") #padding

    down_sampling_time_span = st.empty() #When the radio buttons and number input are enabled, they will appear in the position on the page
    downsampling_value = st.empty()
    downsampling_on_off = st.toggle("Downsampling On/Off", key="downsample_toggle_clickhouse")
    if downsampling_on_off:
        down_sampling_time_span.radio("Downsampling Timeframe:", ["Seconds", "Minutes", "Hours", "Days", "Weeks", "Months", "Years"], key="clickhouse_downsample_time")
        downsampling_value = st.number_input("Downsample Value:", min_value=5, max_value=5000, key="downsample_value_clickhouse")

    st.write("") #padding

    run_query_submit = st.button("Submit", key="submit_clickhouse")
    clickhouse_out_raw_title = st.empty()
    total_elapsed_time_clickhouse_raw = st.empty() #Empty templates in the place they will appear on the UI. Can be called at any time using any widget
    clickhouse_out = st.empty()
    clickhouse_out_downsampled_title = st.empty()
    total_elapsed_time_clickhouse_downsampled = st.empty() #Empty templates in the place they will appear on the UI. Can be called at any time using any widget
    clickhouse_out_downsampled = st.empty()

    if run_query_submit:
        submit_clicked_clickhouse(total_elapsed_time_clickhouse_downsampled, total_elapsed_time_clickhouse_raw, downsampling_on_off, clickhouse_out_raw_title, clickhouse_out, 
                                  clickhouse_out_downsampled_title, clickhouse_out_downsampled, start_date_clickhouse, start_time_clickhouse, end_date_clickhouse, end_time_clickhouse, downsampling_value)

st.markdown("<h1 style='text-align: center;'>Database Benchmarking</h1>", unsafe_allow_html=True)
clickhouse_data_benchmarking_setup()
