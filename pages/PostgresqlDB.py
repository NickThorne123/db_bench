from datetime import date, datetime as dt
from dotenv import load_dotenv
#from postgresql_driver import Client
import streamlit as st
#from streamlit_option_menu import option_menu
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

HOST="localhost"
PORT = 5432
DATABASE="postgres"
USER="postgres"
PASSWORD="postgres"

st.set_page_config(page_title="PostgreSQL | DB Bench", page_icon="./icons/pageIcon.png")
st.markdown("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True) #Shows radio buttons in a row. Streamlit default is vertical list

def init_connection():
    connection = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    return connection 


def submit_clicked_postgres(total_elapsed_time_postgres_downsampled, total_elapsed_time_postgres_raw, downsampling_on_off, postgres_out_raw_title, postgres_out, 
                                  postgres_out_downsampled_title, postgres_out_downsampled, postgresql_start_datetime, postgresql_end_datetime, downsampling_value, 
                                  total_ram_usage_postgres_raw, total_rows_text, total_disk_usage_postgres):
    process = psutil.Process()
    try:
        connection = init_connection()

        total_rows =  pd.read_sql_query('SELECT count(*) FROM demo_ts', connection)
        total_rows_text.text(f"Total Rows in Clickhouse Table: {total_rows.iloc[0]['count']:,}")

        data_process_start_time_raw = time.time() #Gets the start time before the data is processed
        #Get postgres table size
        total_table_size = pd.read_sql_query("SELECT pg_size_pretty( pg_total_relation_size('demo_ts'))", connection)
        total_disk_usage_postgres.text(f"Total Disk Usage for Postgres Table: {total_table_size.iloc[0]['pg_size_pretty']}")

        res_count = pd.read_sql_query(f""" SELECT count(*) FROM demo_ts WHERE cdatetime BETWEEN DATE('{postgresql_start_datetime}') AND DATE('{postgresql_end_datetime}') """, connection).iloc[0]['count']

        memory_usage_pre_raw = process.memory_info().rss / 1024 ** 2 #Gets the amount of RAM used before the process is being run in MB

        res_list =  pd.read_sql_query(f""" SELECT cdatetime, ts_values FROM demo_ts
                    WHERE cdatetime BETWEEN DATE('{postgresql_start_datetime}') AND DATE('{postgresql_end_datetime}')
                    ORDER BY cdatetime DESC LIMIT 500000 """, connection)

        df = pd.DataFrame(res_list, columns =['cdatetime','ts_values'])
        fig = px.line(df, x='cdatetime', y='ts_values')
        fig.update_layout(xaxis_title='Date and Time', yaxis_title = 'Raw Value')
        fig.update_xaxes(range=[postgresql_start_datetime, postgresql_end_datetime]) # Don't let chart autoscale as loses impact of how few samples we're pulling compared to downsampled
        postgres_out_raw_title.markdown("<h4 style='text-align: left;'>Raw Data Chart of 50,000 samples</h4>", unsafe_allow_html=True)
        postgres_out.plotly_chart(fig) # Plots a Plotly chart

        data_process_end_time_raw = time.time() #Gets the end time after data processing is complete
        memory_usage_post_raw = process.memory_info().rss / 1024 ** 2 #Gets the amount of RAM used before the process is being run in MB

        total_elapsed_time_postgres_raw.text(f"Raw Samples Execution time: {round(data_process_end_time_raw - data_process_start_time_raw, 3)} seconds")
        total_ram_usage_postgres_raw.text(f"RAM Usage: {round(memory_usage_post_raw - memory_usage_pre_raw, 2)}MB") #Shows the elapsed time and RAM usage to 3dp above the charts

        if downsampling_on_off: # If the downsampling toggle is selected and True
            data_process_start_time_downsampled = time.time() #Gets the start time before the data is processed
            downsample_query = f"""SELECT cdatetime, ts_values FROM (SELECT cdatetime, ts_values,
                                    row_number() OVER (ORDER BY cdatetime ROWS UNBOUNDED PRECEDING) AS rn
                                    FROM  demo_ts
                                    WHERE  DATE(cdatetime) >= DATE('{postgresql_start_datetime}') and DATE(cdatetime) <= DATE('{postgresql_end_datetime}'))
                                    x WHERE rn % (SELECT COUNT(*) / {downsampling_value} FROM demo_ts WHERE DATE(cdatetime) >= DATE('{postgresql_start_datetime}') and DATE(cdatetime) <= DATE('{postgresql_end_datetime}')) = 0;"""
            df_agg = pd.read_sql_query(downsample_query, connection)
            fig_agg_row_count = df_agg.shape[0]
            fig_agg = px.line(df_agg, x='cdatetime', y='ts_values')
            fig_agg.update_layout(xaxis_title='Date and Time', yaxis_title = 'Downsampled Value')
            fig_agg.update_xaxes(range=[postgresql_start_datetime, postgresql_end_datetime])
            postgres_out_downsampled_title.markdown(f"<h4 style='text-align: left;'>Downsampled Data Chart ({fig_agg_row_count}/{downsampling_value} of {res_count:,} rows)</h4>", unsafe_allow_html=True)
            postgres_out_downsampled.plotly_chart(fig_agg) #Plots a Plotly chart
            data_process_end_time_downsampled = time.time() #Gets the start time before the data is processed
            total_elapsed_time_postgres_downsampled.text(f"Downsampled Execution time: {round(data_process_end_time_downsampled - data_process_start_time_downsampled, 3)} seconds") #Shows the elapsed time to 3dp above the charts
    except (Exception) as error:
        print("Error while connecting to PostgreSQL", error)


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

    downsampling_value = st.empty()
    downsampling_on_off = st.toggle("Downsampling On/Off", key="downsample_toggle_postgresql")
    if downsampling_on_off:
        downsampling_value = st.number_input("Downsample Value:", min_value=5, max_value=5000, key="downsample_value_postgresql")

    st.write("") #padding

    #GUI chart widget placement
    run_query_submit = st.button("Submit", key="submit_postgresql")
    total_rows_text = st.empty()
    total_disk_usage_postgres = st.empty() #Total disk usage

    st.write("") #padding

    postgres_out_raw_title = st.empty()
    total_elapsed_time_postgres_raw = st.empty() #Empty templates in the place they will appear on the UI. Can be called at any time using any widget
    total_ram_usage_postgres_raw = st.empty()
    postgres_out = st.empty()
    postgres_out_downsampled_title = st.empty()
    total_elapsed_time_postgres_downsampled = st.empty() #Empty templates in the place they will appear on the UI. Can be called at any time using any widget
    postgres_out_downsampled = st.empty()

    if run_query_submit:
        submit_clicked_postgres(total_elapsed_time_postgres_downsampled, total_elapsed_time_postgres_raw, downsampling_on_off, postgres_out_raw_title, postgres_out,
                                  postgres_out_downsampled_title, postgres_out_downsampled, postgresql_start_datetime, postgresql_end_datetime, downsampling_value,
                                  total_ram_usage_postgres_raw, total_rows_text, total_disk_usage_postgres)

### Show Streamlit GUI
postgresql_data_benchmarking_setup()
