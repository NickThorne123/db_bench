from datetime import date, datetime as dt
from dotenv import load_dotenv
from clickhouse_driver import Client
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import plotly.express as px
import datetime
import pandas as pd
import time
import numpy
import os
import psutil

load_dotenv()

CH_HOST=os.getenv('CH_HOST')
CH_PORT=os.getenv('CH_PORT')
CH_PASSWORD=os.getenv('CH_PASSWORD')
CH_USER=os.getenv('CH_USER')
CH_DBNAME=os.getenv('CH_DBNAME')

filename = "./icons/pageIcon.png"
img = Image.open(filename)
st.set_page_config(page_title="DB Benchmark", page_icon=img)
st.markdown("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True) #Shows radio buttons in a row. Streamlit default is vertical list

### Clickhouse region
def get_ch_client():
    """Create a Clickhouse DB client object (aka connection)"""
    client = Client(host="localhost", port=9001, settings={'use_numpy': True}, user="chuser", password="chuser_pwd") #TODO shouldn't be hard coded
    return client


def submit_clicked_clickhouse(total_elapsed_time_clickhouse_downsampled, total_elapsed_time_clickhouse_raw, downsampling_on_off, clickhouse_out_raw_title, clickhouse_out,
                               clickhouse_out_downsampled_title, clickhouse_out_downsampled, clickhouse_start_datetime, clickhouse_end_datetime, downsampling_value, 
                               total_ram_usage_clickhouse_raw, total_ram_usage_clickhouse_downsampled):
    """Performs the logic to get the data from the clickhouse DB and outputs it onto streamlit when submit is clicked"""
    client = get_ch_client()
    process = psutil.Process()

    try:
        #Get total row count
        total_rows_query =  f""" SELECT count(*) FROM ts_db.demo_ts  """
        total_rows = client.execute(total_rows_query, settings={'use_numpy': True})[0][0]

        res_count_query =  f""" SELECT count(*) FROM ts_db.demo_ts WHERE cdatetime BETWEEN toDateTime('{clickhouse_start_datetime}') AND toDateTime('{clickhouse_end_datetime}') """
        res_count = client.execute(res_count_query, settings={'use_numpy': True})[0][0]

        memory_usage_pre_raw = process.memory_info().rss / 1024 ** 2 #Gets the amount of RAM used before the process is being run in MB
        res_list_query =  f""" SELECT cdatetime, ts_values FROM ts_db.demo_ts 
                    WHERE cdatetime BETWEEN toDateTime('{clickhouse_start_datetime}') AND toDateTime('{clickhouse_end_datetime}')
                    ORDER BY cdatetime DESC LIMIT 500000 """
        res_list = client.execute(res_list_query, settings={'use_numpy': True})

        data_process_start_time_raw = time.time() #Gets the start time before the data is processed
        df = pd.DataFrame(res_list, columns =['cdatetime','ts_values'])
        fig = px.line(df, x='cdatetime', y='ts_values')
        fig.update_layout(xaxis_title='Date and Time', yaxis_title = 'Raw Value')
        fig.update_xaxes(range=[clickhouse_start_datetime, clickhouse_end_datetime]) # Don't let chart autoscale as loses impact of how few samples we're pulling compared to downsampled
        clickhouse_out_raw_title.write(f"Raw Data Chart of 500,000 samples - {total_rows:,} Total Rows")
        clickhouse_out.plotly_chart(fig) #Plots a Plotly chart

        data_process_end_time_raw = time.time() #Gets the end time after data processing is complete
        memory_usage_post_raw = process.memory_info().rss / 1024 ** 2 #Gets the amount of RAM used as the process is being run in MB

        total_elapsed_time_clickhouse_raw.text(f"Raw Samples Execution time: {round(data_process_end_time_raw - data_process_start_time_raw, 3)} seconds") 
        total_ram_usage_clickhouse_raw.text(f"RAM Usage: {round(memory_usage_post_raw - memory_usage_pre_raw, 2)}MB") #Shows the elapsed time and RAM usage to 3dp above the charts

        if downsampling_on_off: #If the downsampling toggle is selected and True
            memory_usage_pre_downsampled = process.memory_info().rss / 1024 ** 2 #Gets the amount of RAM used as the process is being run in MB
            data_process_start_time_downsampled = time.time() #Gets the start time before the data is processed

            #Shows downsampled values
            downsample_query = f""" FROM ts_db.demo_ts select untuple(arrayJoin(largestTriangleThreeBuckets({downsampling_value})(cdatetime, ts_values )))
                        where toDateTime(cdatetime) >= toDateTime('{clickhouse_start_datetime}') and toDateTime(cdatetime) <= toDateTime('{clickhouse_end_datetime}') """
            res_list_agg = client.execute(downsample_query, settings={'use_numpy': True})
            df_agg = pd.DataFrame(res_list_agg, columns =['cdatetime','ts_values'])
            fig_agg_row_count = df_agg.shape[0]
            fig_agg = px.line(df_agg, x='cdatetime', y='ts_values')
            fig_agg.update_layout(xaxis_title='Date and Time', yaxis_title = 'Downsampled Value')
            clickhouse_out_downsampled_title.write(f"Downsampled Data Chart ({fig_agg_row_count}/{downsampling_value} of {res_count:,} rows)")
            clickhouse_out_downsampled.plotly_chart(fig_agg) #Plots a Plotly chart

            data_process_end_time_downsampled = time.time() #Gets the start time before the data is processed
            memory_usage_post_downsampled = process.memory_info().rss / 1024 ** 2 #Gets the amount of RAM used as the process is being run in MB

            total_elapsed_time_clickhouse_downsampled.text(f"Downsampled Execution time: {round(data_process_end_time_downsampled - data_process_start_time_downsampled, 3)} seconds") #Shows the elapsed time to 3dp above the charts
            total_ram_usage_clickhouse_downsampled.text(f"RAM Usage: {round(memory_usage_pre_downsampled - memory_usage_post_downsampled, 2)}MB") #Shows the elapsed time and RAM usage to 3dp above the charts (RAM usage is higher directly after raw processing hence pre - post)
    except Exception as a:
        print(f'update_output error {a}')
        st.error(f'update_output error {a}')


def clickhouse_data_benchmarking_setup():
    """Displays the layout of the clickhouse widgets in streamlit"""
    col1, col2 = st.columns([1,11])
    with col1:
        st.image("./icons/clickhouseLogo.png", width=50)
    with col2:
        st.markdown("<h3 style='text-align: left;'>ClickhouseDB</h3>", unsafe_allow_html=True)

    start_time_date_col, end_time_date_col = st.columns([1, 1]) #Creates columns for the start and end date / time pickers
    with start_time_date_col:
        start_date_clickhouse = st.date_input("Data Start Date:", datetime.date(2021, 1, 1), key="start_date_clickhouse")
        start_time_clickhouse = st.time_input("Data Start Time:", key="start_time_clickhouse")
    with end_time_date_col:
        end_date_clickhouse = st.date_input("Data End Date:", datetime.date(2022, 1, 2), key="end_date_clickhouse")
        end_time_clickhouse = st.time_input("Data End Time:", key="end_time_clickhouse")
    clickhouse_start_datetime = datetime.datetime.combine(start_date_clickhouse, start_time_clickhouse) #concatenates the date and time
    clickhouse_end_datetime = datetime.datetime.combine(end_date_clickhouse, end_time_clickhouse)

    st.write("") #padding

    #down_sampling_time_span = st.empty() #When the radio buttons and number input are enabled, they will appear in the position on the page # NOTE possibly unecessary
    downsampling_value = st.empty()
    downsampling_on_off = st.toggle("Downsampling On/Off", key="downsample_toggle_clickhouse")
    if downsampling_on_off:
        #down_sampling_time_span.radio("Downsampling Timeframe:", ["Seconds", "Minutes", "Hours", "Days", "Weeks", "Months", "Years"], key="clickhouse_downsample_time") # NOTE possibly unecessary
        downsampling_value = st.number_input("Downsample Value:", min_value=5, max_value=5000, key="downsample_value_clickhouse")

    st.write("") #padding

    #GUI chart widget placement
    run_query_submit = st.button("Submit", key="submit_clickhouse")
    clickhouse_out_raw_title = st.empty()
    total_elapsed_time_clickhouse_raw = st.empty() #Empty templates in the place they will appear on the UI. Can be called at any time using any widget
    total_ram_usage_clickhouse_raw = st.empty()
    clickhouse_out = st.empty()
    clickhouse_out_downsampled_title = st.empty()
    total_elapsed_time_clickhouse_downsampled = st.empty() #Empty templates in the place they will appear on the UI. Can be called at any time using any widget
    total_ram_usage_clickhouse_downsampled = st.empty()
    clickhouse_out_downsampled = st.empty()

    if run_query_submit:
        submit_clicked_clickhouse(total_elapsed_time_clickhouse_downsampled, total_elapsed_time_clickhouse_raw, downsampling_on_off, clickhouse_out_raw_title, clickhouse_out, 
                                  clickhouse_out_downsampled_title, clickhouse_out_downsampled, clickhouse_start_datetime, clickhouse_end_datetime, downsampling_value, 
                                  total_ram_usage_clickhouse_raw, total_ram_usage_clickhouse_downsampled)
        

### PostgreSQL Region
        
def postgresql_data_benchmarking_setup():
    """Displays the layout of the postgreSQL widgets in streamlit"""
    col1, col2 = st.columns([1,11])
    with col1:
        st.image("./icons/postgresqlLogo.png", width=50)
    with col2:
        st.markdown("<h3 style='text-align: left;'>PostgreSQL</h3>", unsafe_allow_html=True)

    start_time_date_col, end_time_date_col = st.columns([1, 1]) #Creates columns for the start and end date / time pickers
    with start_time_date_col:
        start_date_postgresql = st.date_input("Data Start Date:", datetime.date(2021, 1, 1), key="start_date_postgresql")
        start_time_postgresql = st.time_input("Data Start Time:", key="start_time_postgresql")
    with end_time_date_col:
        end_date_postgresql = st.date_input("Data End Date:", datetime.date(2022, 1, 2), key="end_date_postgresql")
        end_time_postgresql = st.time_input("Data End Time:", key="end_time_postgresql")
    postgresql_start_datetime = datetime.datetime.combine(start_date_postgresql, start_time_postgresql) #concatenates the date and time
    postgresql_end_datetime = datetime.datetime.combine(end_date_postgresql, end_time_postgresql)

    st.write("") #padding


### TimescaleDB Region
    
def timescaledb_data_benchmarking_setup():
    """Displays the layout of the timescaledb widgets in streamlit"""
    col1, col2 = st.columns([1,10])
    with col1:
        st.image("./icons/TimeScaleLogo.png", width=50)
    with col2:
        st.markdown("<h3 style='text-align: left;'>TimescaleDB</h3>", unsafe_allow_html=True)

    start_time_date_col, end_time_date_col = st.columns([1, 1]) #Creates columns for the start and end date / time pickers
    with start_time_date_col:
        start_date_timescaledb = st.date_input("Data Start Date:", datetime.date(2021, 1, 1), key="start_date_timescaledb")
        start_time_timescaledb = st.time_input("Data Start Time:", key="start_time_timescaledb")
    with end_time_date_col:
        end_date_timescaledb= st.date_input("Data End Date:", datetime.date(2022, 1, 2), key="end_date_timescaledb")
        end_time_timescaledb = st.time_input("Data End Time:", key="end_time_timescaledb")
    timescaledb_start_datetime = datetime.datetime.combine(start_date_timescaledb, start_time_timescaledb) #concatenates the date and time
    timescaledb_end_datetime = datetime.datetime.combine(end_date_timescaledb, end_time_timescaledb)

    st.write("") #padding


### Streamlit GUI
        
selected = option_menu(
    menu_title=None,
    options=["Home", "ClickHouse", "PostgreSQL", "TimescaleDB"],
    icons=["house", "kanban", "database-fill", "graph-down"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "blue", "font-size": "20px"},
        "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#89cff0"},
    }

)

### Home Page
if selected == "Home":
    col1, col2 = st.columns([1,7])
    with col1:
        st.image(filename, width=70)
    with col2:
        st.markdown("<h1 style='text-align: left;'>Database Benchmarking</h1>", unsafe_allow_html=True)

    
    st.write("""This application is a streamlit web app which plots scalar values over time, 
             with a start / end datetime picker and a database source picker. Created by students at Southampton Solent University for one of our modules, 
             these students are:
             Josh Clarke, Daniel Agha, Iona Pitt, Kyle Roberts and Luke Wood""")
    
    st.write("The database source options for this application are:")

    col3, col4 = st.columns([1,10])
    with col3:
        st.image("./icons/clickhouseLogo.png", width=45)
    with col4:
        st.markdown("<h3 style='text-align: left;'>ClickhouseDB</h3>", unsafe_allow_html=True)

    with col3:
        st.image("./icons/postgresqlLogo.png", width=45)
    with col4:
        st.markdown("<h3 style='text-align: left;'>PostgreSQL</h3>", unsafe_allow_html=True)

    with col3:
        st.image("./icons/TimescaleLogo.png", width=45)
    with col4:
        st.markdown("<h3 style='text-align: left;'>TimescaleDB</h3>", unsafe_allow_html=True)

    st.write("On each page there is: ")
    st.markdown("- A date and time picker, for the start / end date that the data is plotted")
    st.markdown("- A submit button that when pressed fetches the data for the plot")
    st.markdown("- A ‘downsampling on-off’ toggle")
    st.markdown("- A downsampling count text entry.")


    st.write("""
                On pressing ‘submit’ a timer is started that times how long it takes to fetch the data 
                (note this will not include the time taken for the charting library to load it). 
                The elapsed time will be displayed on the dashboard near the line chart. 
                Text boxes will be populated showing the space taken up on disk for the table, 
                and the number of rows in the table. 
                A text box showing GB of disk storage per million rows will be shown.
                """)


### Clickhouse Page
if selected == "ClickHouse":
    clickhouse_data_benchmarking_setup()


### PostgreSQL Page
if selected == "PostgreSQL":
    postgresql_data_benchmarking_setup()


### TimescaleDB Page
if selected == "TimescaleDB":
    timescaledb_data_benchmarking_setup()


