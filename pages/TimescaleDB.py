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

CH_HOST=os.getenv('CH_HOST')
CH_PORT=os.getenv('CH_PORT')
CH_PASSWORD=os.getenv('CH_PASSWORD')
CH_USER=os.getenv('CH_USER')
CH_DBNAME=os.getenv('CH_DBNAME')

st.set_page_config(page_title="TimescaleDB | DB Bench", page_icon="./icons/pageIcon.png")
st.markdown("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True) #Shows radio buttons in a row. Streamlit default is vertical list

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


### Show Streamlit GUI
timescaledb_data_benchmarking_setup()