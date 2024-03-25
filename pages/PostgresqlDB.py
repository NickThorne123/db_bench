from datetime import date, datetime as dt
from dotenv import load_dotenv
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
import psycopg2

load_dotenv()

# CH_HOST=os.getenv('CH_HOST')
# CH_PORT=os.getenv('CH_PORT')
# CH_PASSWORD=os.getenv('CH_PASSWORD')
# CH_USER=os.getenv('CH_USER')
# CH_DBNAME=os.getenv('CH_DBNAME')

st.set_page_config(page_title="PostgreSQL | DB Bench", page_icon="./icons/pageIcon.png")
st.markdown("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True) #Shows radio buttons in a row. Streamlit default is vertical list

host="localhost"
port = 5432
database="postgres"
user="postgres"
password="postgres"

def init_connection():
    connection = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    return connection 
        
def postgresql_data_benchmarking_setup():
    """Displays the layout of the postgreSQL widgets in Streamlit"""
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

    #down_sampling_time_span = st.empty() #When the radio buttons and number input are enabled, they will appear in the position on the page # NOTE possibly unecessary
    downsampling_value = st.empty()
    downsampling_on_off = st.toggle("Downsampling On/Off", key="downsample_toggle_clickhouse")
    if downsampling_on_off:
        #down_sampling_time_span.radio("Downsampling Timeframe:", ["Seconds", "Minutes", "Hours", "Days", "Weeks", "Months", "Years"], key="clickhouse_downsample_time") # NOTE possibly unecessary
        downsampling_value = st.number_input("Downsample Value:", min_value=5, max_value=5000, key="downsample_value_clickhouse")

    st.write("") #padding

    #GUI chart widget placement
    run_query_submit = st.button("Submit", key="submit_postgres")
    postgres_out_raw_title = st.empty()
    total_elapsed_time_postgres_raw = st.empty() #Empty templates in the place they will appear on the UI. Can be called at any time using any widget
    total_ram_usage_postgres_raw = st.empty()
    postgres_out = st.empty()
    postgres_out_downsampled_title = st.empty()
    total_elapsed_time_postgres_downsampled = st.empty() #Empty templates in the place they will appear on the UI. Can be called at any time using any widget
    total_ram_usage_postgres_downsampled = st.empty()
    postgres_out_downsampled = st.empty()

    if run_query_submit:
        submit_clicked_postgres(total_elapsed_time_postgres_downsampled, total_elapsed_time_postgres_raw, downsampling_on_off, postgres_out_raw_title, postgres_out, 
                                  postgres_out_downsampled_title, postgres_out_downsampled, postgresql_start_datetime, postgresql_end_datetime, downsampling_value, 
                                  total_ram_usage_postgres_raw, total_ram_usage_postgres_downsampled)
        
def submit_clicked_postgres(total_elapsed_time_postgres_downsampled, total_elapsed_time_postgres_raw, downsampling_on_off, postgres_out_raw_title, postgres_out, 
                                  postgres_out_downsampled_title, postgres_out_downsampled, postgresql_start_datetime, postgresql_end_datetime, downsampling_value, 
                                  total_ram_usage_postgres_raw, total_ram_usage_postgres_downsampled):
    try:
        connection = init_connection()
        my_table = pd.read_sql('select * from demo_ts', connection)
        print (my_table)
        cdatetime = pd.read_sql_query('select cdatetime from demo_ts', connection)
        ts_values = pd.read_sql_query('select ts_values from demo_ts', connection)
        df = pd.concat([cdatetime.reset_index(drop=True), ts_values.reset_index(drop=True)], axis=1)
        # st.table(data) # For debugging purposes
        data_process_start_time_raw = time.time() #Gets the start time before the data is processed
        fig = px.line(df, x='cdatetime', y='ts_values')
        fig.update_layout(xaxis_title='Date and Time', yaxis_title = 'Raw Value')
        fig.update_xaxes(range=[postgresql_start_datetime, postgresql_end_datetime]) # Don't let chart autoscale as loses impact of how few samples we're pulling compared to downsampled
        postgres_out_raw_title.write(f"Raw Data Chart of ~18,000 samples")
        postgres_out.plotly_chart(fig) # Plots a Plotly chart
        data_process_end_time_raw = time.time() #Gets the end time after data processing is complete
        total_elapsed_time_postgres_raw.text(f"Raw Samples Execution time: {round(data_process_end_time_raw - data_process_start_time_raw, 3)} seconds")

        if downsampling_on_off: # If the downsampling toggle is selected and True
            query = f""" FROM demo_ts select untuple(arrayJoin(largestTriangleThreeBuckets({downsampling_value})(cdatetime, ts_values )))
                        where toDateTime(cdatetime) >= toDateTime('{postgresql_start_datetime}') and toDateTime(cdatetime) <= toDateTime('{postgresql_end_datetime}') """ # This don't work
            downsample_query = 'SELECT cdatetime, ts_values, ROW_NUMBER() OVER (ORDER BY cdatetime) FROM demo_ts' # This do work
            df_agg = pd.read_sql_query(downsample_query, connection)
            print(df_agg)
            fig_agg_row_count = df_agg.shape[0]
            fig_agg = px.line(df_agg, x='cdatetime', y='ts_values')
            fig_agg.update_layout(xaxis_title='Date and Time', yaxis_title = 'Downsampled Value')
            postgres_out_downsampled_title.write(f"Downsampled Data Chart ({fig_agg_row_count}/{downsampling_value})")
            postgres_out_downsampled.plotly_chart(fig_agg) #Plots a Plotly chart
    except (Exception) as error:
        print("Error while connecting to PostgreSQL", error)

### Show Streamlit GUI
postgresql_data_benchmarking_setup()