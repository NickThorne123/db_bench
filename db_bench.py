from datetime import date, datetime as dt
from dotenv import load_dotenv
from clickhouse_driver import Client
import streamlit as st
import plotly.express as px
import threading
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
    client = Client(host=CH_HOST, port=CH_PORT, settings={'use_numpy': True}, user=CH_USER, password=CH_PASSWORD)
    return client


def submit_clicked_postgres(total_elapsed_time_postgres, downsampling_on_off, postgres_out_raw_title, postgres_out, postgres_out_downsampled_title, postgres_out_downsampled, fig_untabbed): #Add the multithreading timer in this function, after a submit button is clicked the timer is started in another thread. When the data is complete the UI displays the total time to display the data.
    data_process_start_time = time.time()
    postgres_out_raw_title.write("Raw Data Chart")
    postgres_out.plotly_chart(fig_untabbed)
    if downsampling_on_off:
        postgres_out_downsampled_title.write("Downsampled Data Chart")
        postgres_out_downsampled.plotly_chart(fig_untabbed)
    data_process_end_time = time.time()
    total_elapsed_time_postgres.text(f"Execution time: {round(data_process_end_time - data_process_start_time, 3)} seconds") #Shows the elapsed time to 3dp


def postgres_data_benchmarking_setup():
    """Plots the timeseries of postgres data for analysis and downsampling"""

    ### #NOTE THIS IS ONLY TEST DATA TO SHOW THE TIME SERIES CHART IT WILL NOT BE USED ###
    df = px.data.stocks()
    fig_untabbed = px.line(df, x='date', y="GOOG")
    ######################################################################################

    st.subheader("Postgres")

    start_time_date_col, end_time_date_col = st.columns([1, 1]) #Creates columns for the start and end date / time pickers
    with start_time_date_col:
        start_date_postgres = st.date_input("Data Start Date:", key="start_date_postgres")
        start_time_postgres = st.time_input("Data Start Time:", key="start_time_postgres")
    with end_time_date_col:
        end_date_postgres = st.date_input("Data End Date:", key="end_date_postgres")
        end_time_postgres = st.time_input("Data End Time:", key="end_time_postgres")

    st.write("") #padding

    down_sampling_time_span = st.empty() #When the radio buttons and number input are enabled, they will appear in the position on the page
    downsampling_value = st.empty()

    downsampling_on_off = st.toggle("Downsampling On/Off", key="downsample_toggle_postgres")
    if downsampling_on_off:
        down_sampling_time_span.radio("Downsampling Timeframe:", ["Seconds", "Minutes", "Hours", "Days", "Weeks", "Months", "Years"], key="postgres_downsample_time")
        downsampling_value.number_input("Downsample Value:", key="downsample_value_postgres")

    st.write("") #padding

    run_query_submit = st.button("Submit", key="submit_postgres")
    total_elapsed_time_postgres = st.empty() #Empty templates in the place they will appear on the UI. Can be called at any time using any widget
    postgres_out_raw_title = st.empty()
    postgres_out = st.empty()
    postgres_out_downsampled_title = st.empty()
    postgres_out_downsampled = st.empty()

    if run_query_submit:
        submit_clicked_postgres(total_elapsed_time_postgres, downsampling_on_off, postgres_out_raw_title, postgres_out, postgres_out_downsampled_title, postgres_out_downsampled, fig_untabbed)

st.markdown("<h1 style='text-align: center;'>Database Benchmarking</h1>", unsafe_allow_html=True)
postgres_data_benchmarking_setup()
