from datetime import datetime
from dotenv import load_dotenv
from clickhouse_driver import Client
import streamlit as st
import plotly.express as px
import datetime
import pandas as pd
import time
import os
import psutil

load_dotenv(override=True)

CH_HOST=os.getenv('CH_HOST')
CH_PORT=os.getenv('CH_PORT')
CH_PASSWORD=os.getenv('CH_PASSWORD')
CH_USER=os.getenv('CH_USER')
CH_DBNAME=os.getenv('CH_DBNAME')

st.set_page_config(page_title="ClickhouseDB | DB Bench", page_icon="./icons/pageIcon.png")
st.markdown("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True) #Shows radio buttons in a row. Streamlit default is vertical list

def get_ch_client():
    """Create a Clickhouse DB client object (aka connection)"""
    client = Client(host=CH_HOST, port=CH_PORT, settings={'use_numpy': True}, user=CH_USER, password=CH_PASSWORD)
    return client


def submit_clicked_clickhouse(total_elapsed_time_clickhouse_downsampled, total_elapsed_time_clickhouse_raw, downsampling_on_off, clickhouse_out_raw_title, clickhouse_out,
                               clickhouse_out_downsampled_title, clickhouse_out_downsampled, clickhouse_start_datetime, clickhouse_end_datetime, downsampling_value,
                               total_ram_usage_clickhouse_raw, total_disk_usage_clickhouse, total_rows_text):
    """Performs the logic to get the data from the clickhouse DB and outputs it onto streamlit when submit is clicked"""
    client = get_ch_client()
    process = psutil.Process()

    try:
        #Get total row count
        total_rows_query =  f""" SELECT count(*) FROM ts_db.demo_ts  """
        total_rows = client.execute(total_rows_query, settings={'use_numpy': True})[0][0]

        total_rows_text.text(f"Total Rows in Clickhouse Table: {total_rows:,}")

        #Get clickhouse table size _ Int = 4 bytes and Datetime = 4 bytes in Clickhouse
        #NOTE if an SQL command to check the table size can be found then use that instead but this should be accurate
        total_table_size = round(((total_rows * 8) / 1024 ** 2), 2)
        if total_table_size >= 1024: #If size is over 1024MB, divide by 1024 and show as GB
            total_disk_usage_clickhouse.text(f"Total Disk Usage for Clickhouse Table: {round(total_table_size / 1024, 2)}GB")
        else:
            total_disk_usage_clickhouse.text(f"Total Disk Usage for Clickhouse Table: {total_table_size}MB")

        res_count_query =  f""" SELECT count(*) FROM ts_db.demo_ts WHERE cdatetime BETWEEN toDateTime('{clickhouse_start_datetime}') AND toDateTime('{clickhouse_end_datetime}') """
        res_count = client.execute(res_count_query, settings={'use_numpy': True})[0][0]

        memory_usage_pre_raw = process.memory_info().rss / 1024 ** 2 #Gets the amount of RAM used before the process is being run in MB
        data_process_start_time_raw = time.time() #Gets the start time before the data is processed
        res_list_query =  f""" SELECT cdatetime, ts_values FROM ts_db.demo_ts 
                    WHERE cdatetime BETWEEN toDateTime('{clickhouse_start_datetime}') AND toDateTime('{clickhouse_end_datetime}')
                    ORDER BY cdatetime DESC LIMIT 50000 """
        res_list = client.execute(res_list_query, settings={'use_numpy': True})
        data_process_end_time_raw = time.time() #Gets the end time after data processing is complete
        df = pd.DataFrame(res_list, columns =['cdatetime','ts_values'])
        fig = px.line(df, x='cdatetime', y='ts_values')
        fig.update_layout(xaxis_title='Date and Time', yaxis_title = 'Raw Value')
        fig.update_xaxes(range=[clickhouse_start_datetime, clickhouse_end_datetime]) # Don't let chart autoscale as loses impact of how few samples we're pulling compared to downsampled
        clickhouse_out_raw_title.markdown("<h4 style='text-align: left;'>Raw Data Chart of 50,000 samples</h4>", unsafe_allow_html=True)
        clickhouse_out.plotly_chart(fig) #Plots a Plotly chart

        memory_usage_post_raw = process.memory_info().rss / 1024 ** 2 #Gets the amount of RAM used as the process is being run in MB

        total_elapsed_time_clickhouse_raw.text(f"Raw Samples Data Collection time: {round(data_process_end_time_raw - data_process_start_time_raw, 3)} seconds")
        total_ram_usage_clickhouse_raw.text(f"RAM Usage: {round(memory_usage_post_raw - memory_usage_pre_raw, 2)}MB") #Shows the elapsed time and RAM usage to 3dp above the charts

        if downsampling_on_off: #If the downsampling toggle is selected and True
            data_process_start_time_downsampled = time.time() #Gets the start time before the data is processed

            #Shows downsampled values
            downsample_query = f""" FROM ts_db.demo_ts SELECT untuple(arrayJoin(largestTriangleThreeBuckets({downsampling_value})(cdatetime, ts_values)))
                        WHERE toDateTime(cdatetime) >= toDateTime('{clickhouse_start_datetime}') and toDateTime(cdatetime) <= toDateTime('{clickhouse_end_datetime}') """
            res_list_agg = client.execute(downsample_query, settings={'use_numpy': True})
            data_process_end_time_downsampled = time.time() #Gets the start time before the data is processed
            df_agg = pd.DataFrame(res_list_agg, columns=['cdatetime','ts_values'])
            fig_agg_row_count = df_agg.shape[0]
            fig_agg = px.line(df_agg, x='cdatetime', y='ts_values')
            fig_agg.update_layout(xaxis_title='Date and Time', yaxis_title = 'Downsampled Value')
            clickhouse_out_downsampled_title.markdown(f"<h4 style='text-align: left;'>Downsampled Data Chart ({fig_agg_row_count}/{downsampling_value} of {res_count:,} rows)</h4>", unsafe_allow_html=True)
            clickhouse_out_downsampled.plotly_chart(fig_agg) #Plots a Plotly chart
            total_elapsed_time_clickhouse_downsampled.text(f"Downsampled Data Collection time: {round(data_process_end_time_downsampled - data_process_start_time_downsampled, 3)} seconds") #Shows the elapsed time to 3dp above the charts
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
        st.subheader("Clickhouse Read Data Benchmarking")

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

    downsampling_value = st.empty()
    downsampling_on_off = st.toggle("Downsampling On/Off", key="downsample_toggle_clickhouse")
    if downsampling_on_off:
        downsampling_value = st.number_input("Downsample Value:", min_value=5, max_value=5000, key="downsample_value_clickhouse")

    st.write("") #padding

    #GUI chart widget placement
    run_query_submit = st.button("Submit", key="submit_clickhouse")
    total_rows_text = st.empty()
    total_disk_usage_clickhouse = st.empty() #Total disk usage

    st.write("") #padding

    clickhouse_out_raw_title = st.empty()
    total_elapsed_time_clickhouse_raw = st.empty() #Empty templates in the place they will appear on the UI. Can be called at any time using any widget)
    total_ram_usage_clickhouse_raw = st.empty()
    clickhouse_out = st.empty()
    clickhouse_out_downsampled_title = st.empty()
    total_elapsed_time_clickhouse_downsampled = st.empty() #Empty templates in the place they will appear on the UI. Can be called at any time using any widget
    clickhouse_out_downsampled = st.empty()

    if run_query_submit:
        if clickhouse_start_datetime > clickhouse_end_datetime:
            st.error("Start date / time cannot be after end date / time")
        else:
            submit_clicked_clickhouse(total_elapsed_time_clickhouse_downsampled, total_elapsed_time_clickhouse_raw, downsampling_on_off, clickhouse_out_raw_title, clickhouse_out, 
                                    clickhouse_out_downsampled_title, clickhouse_out_downsampled, clickhouse_start_datetime, clickhouse_end_datetime, downsampling_value, 
                                    total_ram_usage_clickhouse_raw, total_disk_usage_clickhouse, total_rows_text)


def submit_clicked_clickhouse_write(clickhouse_start_datetime_write, clickhouse_end_datetime_write, total_elapsed_time_clickhouse_write, clickhouse_successful_write, clickhouse_out_total_rows_write,
                                    total_disk_usage_clickhouse_write, clickhouse_data_load_text):
    client = get_ch_client()
    clickhouse_data_load_text.text("Data Being Written...")
    try:
        data_process_start_time_write = time.time() #Gets the start time before the data is written
        clickhouse_write_query =  f""" CREATE TABLE ts_db.demo_write 
                                        ENGINE = MergeTree
                                        ORDER BY tuple()
                                        AS
                                        SELECT toDateTime(arrayJoin(range(toUInt32(toDateTime('{clickhouse_start_datetime_write}')), toUInt32(toDateTime('{clickhouse_end_datetime_write}')), 1) )) as cdatetime,
                                            toSecond(toDateTime(arrayJoin(range(toUInt32(toDateTime('{clickhouse_start_datetime_write}')), toUInt32(toDateTime('{clickhouse_end_datetime_write}')), 1) ))) +
                                            toMinute(toDateTime(arrayJoin(range(toUInt32(toDateTime('{clickhouse_start_datetime_write}')), toUInt32(toDateTime('{clickhouse_end_datetime_write}')), 1) ))) +
                                            2 * toHour(toDateTime(arrayJoin(range(toUInt32(toDateTime('{clickhouse_start_datetime_write}')), toUInt32(toDateTime('{clickhouse_end_datetime_write}')), 1) ))) +
                                            5 * toDayOfWeek(toDateTime(arrayJoin(range(toUInt32(toDateTime('{clickhouse_start_datetime_write}')), toUInt32(toDateTime('{clickhouse_end_datetime_write}')), 1) ))) +
                                            8 * toWeek(toDateTime(arrayJoin(range(toUInt32(toDateTime('{clickhouse_start_datetime_write}')), toUInt32(toDateTime('{clickhouse_end_datetime_write}')), 1) ))) +
                                            12 * toMonth(toDateTime(arrayJoin(range(toUInt32(toDateTime('{clickhouse_start_datetime_write}')), toUInt32(toDateTime('{clickhouse_end_datetime_write}')), 1) ))) +
                                            20 * (toYear(toDateTime(arrayJoin(range(toUInt32(toDateTime('{clickhouse_start_datetime_write}')), toUInt32(toDateTime('{clickhouse_end_datetime_write}')), 1) )))-{clickhouse_end_datetime_write.year}) as ts_values """
        client.execute(clickhouse_write_query, settings={'use_numpy': True}) #Creates the data inside the table
        data_process_end_time_write = time.time() #Gets the end time after the data is written

        total_rows_query_write =  f""" SELECT count(*) FROM ts_db.demo_write  """
        total_rows_write = client.execute(total_rows_query_write, settings={'use_numpy': True})[0][0]

        total_disk_usage_query_write = round(((total_rows_write * 8) / 1024 ** 2), 2)

        clickhouse_data_load_text.empty()
        clickhouse_out_total_rows_write.text(f"Total Rows Written to Clickhouse Table: {total_rows_write:,}")
        clickhouse_successful_write.text("Data successfully written to Clickhouse Database")
        total_elapsed_time_clickhouse_write.text(f"Time to Write Data to Table: {round(data_process_end_time_write - data_process_start_time_write, 3)} seconds")
        
        if total_disk_usage_query_write >= 1024:
            total_disk_usage_clickhouse_write.text(f"Total Disk Usage of Written Data: {round(total_disk_usage_query_write / 1024, 2)}GB")
        else:
            total_disk_usage_clickhouse_write.text(f"Total Disk Usage of Written Data: {total_disk_usage_query_write}MB")
    except:
      st.error("Error writing data to Clickhouse Database")
    try:
        drop_table_query_write = """DROP TABLE ts_db.demo_write""" #Removes the table before its recreated
        client.execute(drop_table_query_write, settings={'use_numpy': True})
        print("Table Removed")
    except:
        print("Table empty")


def clickhouse_data_write_benchmarking_setup():
    #use sql to create a new table if not exist already. If exist, drop the table.
    """Displays the layout of the clickhouse widgets in streamlit to send the data to the database"""
    col1, col2 = st.columns([1,11])
    with col2:
        st.subheader("Clickhouse Write Data Benchmarking")

    start_time_date_col_write, end_time_date_col_write = st.columns([1, 1]) #Creates columns for the start and end date / time pickers
    with start_time_date_col_write:
        start_date_clickhouse_write = st.date_input("Data Start Date:", datetime.date(2021, 1, 1), key="start_date_clickhouse_write")
        start_time_clickhouse_write = st.time_input("Data Start Time:", key="start_time_clickhouse_write")
    with end_time_date_col_write:
        end_date_clickhouse_write = st.date_input("Data End Date:", datetime.date(2022, 1, 2), key="end_date_clickhouse_write")
        end_time_clickhouse_write = st.time_input("Data End Time:", key="end_time_clickhouse_write")
    clickhouse_start_datetime_write = datetime.datetime.combine(start_date_clickhouse_write, start_time_clickhouse_write) #concatenates the date and time
    clickhouse_end_datetime_write = datetime.datetime.combine(end_date_clickhouse_write, end_time_clickhouse_write)

    st.write("") #padding

    #GUI chart widget placement
    run_query_submit_write = st.button("Submit", key="submit_clickhouse_write")
    clickhouse_data_load_text = st.empty()
    clickhouse_successful_write = st.empty()
    st.write("") # padding
    total_disk_usage_clickhouse_write = st.empty() #Total disk usage
    clickhouse_out_total_rows_write = st.empty()
    total_elapsed_time_clickhouse_write = st.empty() #Empty templates in the place they will appear on the UI. Can be called at any time using any widget)

    if run_query_submit_write:
        if clickhouse_start_datetime_write > clickhouse_end_datetime_write:
            st.error("Start date / time cannot be after end date / time")
        else:
            submit_clicked_clickhouse_write(clickhouse_start_datetime_write, clickhouse_end_datetime_write,total_elapsed_time_clickhouse_write, clickhouse_successful_write, clickhouse_out_total_rows_write,
                                            total_disk_usage_clickhouse_write, clickhouse_data_load_text)


### Show Streamlit GUI
clickhouse_data_benchmarking_setup()
st.write("") #padding
st.write("")
st.write("")
st.write("")
st.write("")
clickhouse_data_write_benchmarking_setup()
