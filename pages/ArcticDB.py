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

st.set_page_config(page_title="ArcticDB | DB Bench", page_icon="./icons/pageIcon.png")
st.markdown("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True) #Shows radio buttons in a row. Streamlit default is vertical list

### TimescaleDB Region
    
def arcticdb_data_benchmarking_setup():
    """Displays the layout of the arcticdb widgets in streamlit"""
    col1, col2 = st.columns([1,10])
    with col1:
        st.image("./icons/arcticLogo.png", width=50)
    with col2:
        st.markdown("<h3 style='text-align: left;'>ArcticDB</h3>", unsafe_allow_html=True)

    start_time_date_col, end_time_date_col = st.columns([1, 1]) #Creates columns for the start and end date / time pickers
    with start_time_date_col:
        start_date_arcticdb = st.date_input("Data Start Date:", datetime.date(2021, 1, 1), key="start_date_arcticdb")
        start_time_arcticdb = st.time_input("Data Start Time:", key="start_time_arcticdb")
    with end_time_date_col:
        end_date_arcticdb= st.date_input("Data End Date:", datetime.date(2022, 1, 2), key="end_date_arcticdb")
        end_time_arcticdb = st.time_input("Data End Time:", key="end_time_arcticdb")
    arcticdb_start_datetime = datetime.datetime.combine(start_date_arcticdb, start_time_arcticdb) #concatenates the date and time
    arcticdb_end_datetime = datetime.datetime.combine(end_date_arcticdb, end_time_arcticdb)


    st.write("") #padding

    downsampling_value = st.empty()
    downsampling_on_off = st.toggle("Downsampling On/Off", key="downsample_toggle_arcticdb")
    if downsampling_on_off:
        downsampling_value = st.number_input("Downsample Value:", min_value=5, max_value=5000, key="downsample_value_arcticdb")

    st.write("") #padding

    #GUI chart widget placement
    total_rows_text = st.empty()
    total_disk_usage_arcticdb = st.empty() #Total disk usage
    run_query_submit = st.button("Submit", key="submit_arcticdb")
    arcticdb_out_raw_title = st.empty()
    total_elapsed_time_arcticdb_raw = st.empty() #Empty templates in the place they will appear on the UI. Can be called at any time using any widget)
    total_ram_usage_arcticdb_raw = st.empty()
    arcticdb_out = st.empty()
    arcticdb_out_downsampled_title = st.empty()
    total_elapsed_time_arcticdb_downsampled = st.empty() #Empty templates in the place they will appear on the UI. Can be called at any time using any widget
    arcticdb_out_downsampled = st.empty()

    # if run_query_submit:
    #     submit_clicked_arcticdb(total_elapsed_time_arcticdb_downsampled, total_elapsed_time_arcticdb_raw, downsampling_on_off, arcticdb_out_raw_title, arcticdb_out, 
    #                               arcticdb_out_downsampled_title, arcticdb_out_downsampled, arcticdb_start_datetime, arcticdb_end_datetime, downsampling_value, 
    #                               total_ram_usage_arcticdb_raw, total_disk_usage_arcticdb, total_rows_text)
### Show Streamlit GUI
arcticdb_data_benchmarking_setup()