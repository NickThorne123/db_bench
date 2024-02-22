import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import date, datetime as dt
from clickhouse_driver import Client
import time
import numpy
from dotenv import load_dotenv
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


def submit_clicked():
    return


def postgres_data_benchmarking():
    """Plots the timeseries of postgres data for analysis and downsampling"""

    ### #NOTE THIS IS ONLY TEST DATA TO SHOW THE TIME SERIES CHART IT WILL NOT BE USED ###
    df = px.data.stocks()
    fig_untabbed = px.line(df, x='date', y="GOOG")
    ######################################################################################

    st.subheader("Postgres")

    start_time_date_col, end_time_date_col = st.columns([1, 1]) #Creates columns for the start and end date / time pickers
    with start_time_date_col:
        start_date = st.date_input("Data Start Date:", key="start_date_postgres")
        start_time = st.time_input("Data Start Time:", key="start_time_postgres")
    with end_time_date_col:
        end_date = st.date_input("Data End Date:", key="end_date_postgres")
        end_time = st.time_input("Data End Time:", key="end_time_postgres")

    st.write("") #padding
    st.write("")

    down_sampling_time_span = st.empty() #When the radio buttons and number input are enabled, they will appear in the position on the page
    downsampling_value = st.empty()

    downsampling_col,  aggregate_col = st.columns([1, 2]) #Creates columns for downsampling and aggregate selectors
    with downsampling_col:
        downsampling_on_off = st.toggle("Downsampling On/Off", key="downsample_toggle_postgres")
        if downsampling_on_off:
            down_sampling_time_span.radio("Downsampling Timeframe:", ["Seconds", "Minutes", "Hours", "Days", "Weeks", "Months", "Years"], key="postgres_downsample_time")
            downsampling_value.number_input("Downsample Value:", key="downsample_value_postgres")
        else:
            down_sampling_time_span.empty() #When disabled the widgets are removed
            downsampling_value.empty()
    with aggregate_col:
        aggregate_on_off = st.toggle("Show / Hide Non-Aggregated Chart", key="aggregate_toggle_postgres")

    st.write("") #padding

    run_query_submit = st.button("Submit", key="submit_postgres")

    #TODO set the chart as an empty st widget to begin with so it can be cleared redrawn to show downsampled data?
    postgres_out = st.empty()

    if run_query_submit:
        submit_clicked()
        postgres_out.plotly_chart(fig_untabbed)

st.markdown("<h1 style='text-align: center;'>Database Benchmarking</h1>", unsafe_allow_html=True)
postgres_data_benchmarking()