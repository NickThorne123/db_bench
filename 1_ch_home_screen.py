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


def get_ch_client():
    """Create a Clickhouse DB client object (aka connection)"""
    client = Client(host=CH_HOST, port=CH_PORT, settings={'use_numpy': True}, user=CH_USER, password=CH_PASSWORD)
    return client


def single_db_timeseries_tabbed():
    """Plots the timeseries data of the passed in database - Tabbed"""

    no_downsample_tab, downsampled_tab = st.tabs(["Timeseries No Downsampling", "Timeseries With Downsampling"])

    with no_downsample_tab:
        row_limit_tabbed = st.number_input("Limit for raw rows:", min_value=1, max_value=10000) #Currently does nothing
        ### #NOTE THIS IS ONLY TEST DATA TO SHOW THE TIME SERIES CHART IT WILL NOT BE USED ###
        df = px.data.stocks() 
        fig = px.line(df, x='date', y="GOOG")
        st.plotly_chart(fig)

    with downsampled_tab:
        points_to_downsample_tabbed = st.number_input("Points to downsample:", min_value=1, max_value=5000) #Currently does nothing
        ### #NOTE THIS IS ONLY TEST DATA TO SHOW THE TIME SERIES CHART IT WILL NOT BE USED ###
        df = px.data.stocks() 
        fig = px.line(df, x='date', y="GOOG")
        st.plotly_chart(fig)


def single_db_timeseries_seperated():
    """Plots the timeseries data of the passed in database - Untabbed"""

    ### #NOTE THIS IS ONLY TEST DATA TO SHOW THE TIME SERIES CHART IT WILL NOT BE USED ### 
    df = px.data.stocks()
    fig_untabbed = px.line(df, x='date', y="GOOG")

    st.subheader("Timeseries No Downsampling")
    row_limit_untabbed = st.slider("Limit for raw rows:", min_value=1, max_value=10000) #Currently does nothing
    st.plotly_chart(fig_untabbed)

    st.write("")
    st.write("")

    st.subheader("Timeseries With Downsampling")
    points_to_downsample_untabbed = st.slider("Points to downsample:", min_value=1, max_value=5000) #Currently does nothing
    st.plotly_chart(fig_untabbed)


st.title("Time Series Charts - Tabbed")
single_db_timeseries_tabbed()

st.write("")
st.write("")
st.write("")

st.title("Time Series Charts - Untabbed")
single_db_timeseries_seperated()