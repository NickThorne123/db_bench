from datetime import datetime
from arcticdb import Arctic
from dotenv import load_dotenv
import streamlit as st
import plotly.express as px
import datetime
import pandas as pd
import time
import sys
import psutil
import os

load_dotenv(override=True)

ARCTIC_URL=os.getenv('ARCTIC_URL')

st.set_page_config(page_title="ArcticDB | DB Bench", page_icon="./icons/pageIcon.png")
st.markdown("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True) #Shows radio buttons in a row. Streamlit default is vertical list

def resample(df, downsampling_value, downsample_unit):
    """Function that downsamples the dataframe"""
    resample_value = "{}{}".format(round(len(df)/downsampling_value), downsample_unit)
    return df.resample(resample_value).mean()

def submit_clicked_arcticdb(total_elapsed_time_arcticdb_downsampled, total_elapsed_time_arcticdb_raw, downsampling_on_off, arcticdb_out_raw_title, arcticdb_out, 
                                  arcticdb_out_downsampled_title, arcticdb_out_downsampled, arcticdb_start_datetime, arcticdb_end_datetime, downsampling_value, 
                                  total_ram_usage_arcticdb_raw, total_rows_text, total_disk_usage_arcticdb):
    process = psutil.Process()

    try:
        ac = Arctic(uri="s3s://s3.eu-west-2.amazonaws.com:arcticdbbench?aws_auth=true")
        db_bench_lib = ac["demo_ts"]
        from_storage_df = db_bench_lib.read("demo_ts_frame").data
        df = pd.DataFrame(from_storage_df)
        df.columns = ["cdatetime", "ts_values"]

        res_count = len(df.loc[df["cdatetime"].between(arcticdb_start_datetime, arcticdb_end_datetime)])

        total_rows_text.text(f"Total Rows in ArcticDB Table: {len(from_storage_df):,}")
        data_process_start_time_raw = time.time() #Gets the start time before the data is processed
        #Get arcticdb table size
        total_disk_usage_arcticdb.text(f"Total Disk Usage for ArcticDB Table: {round(sys.getsizeof(from_storage_df) / 1024 ** 2, 2)}MB")
        memory_usage_pre_raw = process.memory_info().rss / 1024 ** 2 #Gets the amount of RAM used before the process is being run in MB

        arctic_df = df.loc[df["cdatetime"].between(arcticdb_start_datetime, arcticdb_end_datetime)].iloc[:50000] #Gets the data between the selected dates and collects 50k samples
        fig = px.line(arctic_df, x="cdatetime", y="ts_values")
        fig.update_layout(xaxis_title='Date and Time', yaxis_title = 'Raw Value')
        fig.update_xaxes(range=[arcticdb_start_datetime, arcticdb_end_datetime])
        arcticdb_out_raw_title.markdown("<h4 style='text-align: left;'>Raw Data Chart of 50,000 samples</h4>", unsafe_allow_html=True)
        arcticdb_out.plotly_chart(fig) # Plots a Plotly chart

        data_process_end_time_raw = time.time() #Gets the end time after data processing is complete
        memory_usage_post_raw = process.memory_info().rss / 1024 ** 2 #Gets the amount of RAM used before the process is being run in MB

        total_elapsed_time_arcticdb_raw.text(f"Raw Samples Execution time: {round(data_process_end_time_raw - data_process_start_time_raw, 3)} seconds")
        total_ram_usage_arcticdb_raw.text(f"RAM Usage: {round(memory_usage_post_raw - memory_usage_pre_raw, 2)}MB") #Shows the elapsed time and RAM usage to 3dp above the charts

        if downsampling_on_off: # If the downsampling toggle is selected and True
            data_process_start_time_downsampled = time.time() #Gets the start time before the data is processed

            df["cdatetime"] = pd.to_datetime(df["cdatetime"])
            mask = (df['cdatetime'] > arcticdb_start_datetime) & (df['cdatetime'] <= arcticdb_end_datetime) #Sets the downsample dataframe to the selected time / date
            df = df.loc[mask]
            df = df.set_index("cdatetime")
            df_agg = resample(df, downsampling_value, "s") #Downsamples the data using the resample function

            fig_agg_row_count = df_agg.shape[0]
            fig_agg = px.line(df_agg, y='ts_values')
            fig_agg.update_layout(xaxis_title='Date and Time', yaxis_title = 'Downsampled Value')
            fig_agg.update_xaxes(range=[arcticdb_start_datetime, arcticdb_end_datetime])
            arcticdb_out_downsampled_title.markdown(f"<h4 style='text-align: left;'>Downsampled Data Chart ({fig_agg_row_count}/{downsampling_value} of {res_count:,} rows)</h4>", unsafe_allow_html=True)
            arcticdb_out_downsampled.plotly_chart(fig_agg) #Plots a Plotly chart
            data_process_end_time_downsampled = time.time() #Gets the start time before the data is processed
            total_elapsed_time_arcticdb_downsampled.text(f"Downsampled Execution time: {round(data_process_end_time_downsampled - data_process_start_time_downsampled, 3)} seconds") #Shows the elapsed time to 3dp above the charts
    except (Exception) as error:
        print("Error while connecting to ArcticDB", error)

    
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
    run_query_submit = st.button("Submit", key="submit_arcticdb")
    total_rows_text = st.empty()
    total_disk_usage_arcticdb = st.empty() #Total disk usage

    st.write("") #padding

    arcticdb_out_raw_title = st.empty()
    total_elapsed_time_arcticdb_raw = st.empty() #Empty templates in the place they will appear on the UI. Can be called at any time using any widget)
    total_ram_usage_arcticdb_raw = st.empty()
    arcticdb_out = st.empty()
    arcticdb_out_downsampled_title = st.empty()
    total_elapsed_time_arcticdb_downsampled = st.empty() #Empty templates in the place they will appear on the UI. Can be called at any time using any widget
    arcticdb_out_downsampled = st.empty()

    if run_query_submit:
        if arcticdb_start_datetime > arcticdb_end_datetime:
            st.error("Start date / time cannot be after end date / time")
        else:
            submit_clicked_arcticdb(total_elapsed_time_arcticdb_downsampled, total_elapsed_time_arcticdb_raw, downsampling_on_off, arcticdb_out_raw_title, arcticdb_out,
                                  arcticdb_out_downsampled_title, arcticdb_out_downsampled, arcticdb_start_datetime, arcticdb_end_datetime, downsampling_value,
                                  total_ram_usage_arcticdb_raw, total_disk_usage_arcticdb, total_rows_text)
### Show Streamlit GUI
arcticdb_data_benchmarking_setup()