import datetime as dt
import pytest
from streamlit.testing.v1 import AppTest

def test_1_selected_tab_option_clickhouse():
        """A test that will select the Clickhouse tab"""
        at = AppTest.from_file("db_bench.py").run()
        assert at.selectbox(key="page_selection").set_value("ClickHouse").select().run()

def test_2_selected_tab_option_postgresql():
        """A test that will select the Postgresql tab"""
        at = AppTest.from_file("db_bench.py").run()
        assert at.selectbox(key="page_selection").set_value("PostgreSQL").select().run()

def test_3_selected_tab_option_timescaledb():
        """A test that will select the Timescale tab"""
        at = AppTest.from_file("db_bench.py").run()
        assert at.selectbox(key="page_selection").set_value("TimescaleDB").select().run()

def test_4_selected_tab_option_home():
        """A test that will select the Home tab"""
        at = AppTest.from_file("db_bench.py").run()
        assert at.selectbox(key="page_selection").set_value("Home").select().run()

def test_5_downsample_clickhouse_enable():
    """A test to check whether the downsample toggle can be clicked to enable it"""
    at = AppTest.from_file("db_bench.py").run()
    assert at.toggle(key="downsample_toggle_clickhouse").run()

def test_6_increment_downsample_value_clickhouse(): #NOTE For some reason this doesn't recognise the key - Will look into it
    """A test to increment the downsample number input"""
    at = AppTest.from_file("db_bench.py").run()
    at.number_input(key="downsample_value_clickhouse").increment().run()
    assert at.number_input(key="downsample_value_clickhouse").value == 1

def test_7_set_start_date_value_clickhouse():
        """A test to set the clickhouse start date"""
        at = AppTest.from_file("db_bench.py").run()
        at.date_input(key="start_date_clickhouse").set_value(dt.date(2024, 1, 1)).run()
        assert at.date_input(key="start_date_clickhouse").value == dt.date(2024, 1, 1)

def test_8_set_end_date_value_clickhouse():
        """A test to set the clickhouse end date"""
        at = AppTest.from_file("db_bench.py").run()
        at.date_input(key="end_date_clickhouse").set_value(dt.date(2019, 6, 6)).run()
        assert at.date_input(key="end_date_clickhouse").value == dt.date(2019, 6, 6)

def test_9_set_start_time_value_clickhouse(): #NOTE For some reason this doesn't recognise the key - Will look into it
        """A test to set the clickhouse start time"""
        at = AppTest.from_file("db_bench.py").run()
        at.time_input(key="start_time_clickhouse").set_value(dt.time(13, 50))
        assert at.date_input(key="start_time_clickhouse").value == (dt.time(13, 50),) #Dates in a weird format for some reason

def test_10_set_end_time_value_clickhouse(): #NOTE For some reason this doesn't recognise the key - Will look into it
        """A test to set the clickhouse end time"""
        at = AppTest.from_file("db_bench.py").run()
        at.time_input(key="end_time_clickhouse").set_value(dt.time(7, 30))
        assert at.date_input(key="end_time_clickhouse").value == (dt.time(7, 30),) #Dates in a weird format for some reason

def test_11_submit_clickhouse(): #NOTE For some reason this doesn't recognise the key - Will look into it
        """A test to click the submit button and start collecting clickhouse data"""
        at = AppTest.from_file("db_bench.py").run()
        assert at.button(key="submit_clickhouse").click().run()
        
def test_12_downsample_postgresql_enable(): #TODO Implement downsample buttons
    """A test to check whether the downsample toggle can be clicked to enable it"""
    at = AppTest.from_file("db_bench.py").run()
    assert at.toggle(key="downsample_toggle_postgresql").run()

def test_13_increment_downsample_value_clickhouse(): #NOTE For some reason this doesn't recognise the key - Will look into it
    """A test to increment the downsample number input"""
    at = AppTest.from_file("db_bench.py").run()
    at.number_input(key="downsample_value_clickhouse").increment().run()
    assert at.number_input(key="downsample_value_clickhouse").value == 1
        
def test_14_set_start_date_value_postgresql():
        """A test to set the postgresql start date"""
        at = AppTest.from_file("db_bench.py").run()
        at.date_input(key="start_date_postgresql").set_value(dt.date(2024, 1, 1)).run()
        assert at.date_input(key="start_date_postgresql").value == dt.date(2024, 1, 1)

def test_15_set_end_date_value_postgresql():
        """A test to set the postgresql end date"""
        at = AppTest.from_file("db_bench.py").run()
        at.date_input(key="end_date_postgresql").set_value(dt.date(2019, 6, 6)).run()
        assert at.date_input(key="end_date_postgresql").value == dt.date(2019, 6, 6)

def test_16_set_start_time_value_postgresql(): #NOTE For some reason this doesn't recognise the key - Will look into it
        """A test to set the postgresql start time"""
        at = AppTest.from_file("db_bench.py").run()
        at.time_input(key="start_time_postgresql").set_value(dt.time(13, 50))
        assert at.date_input(key="start_time_postgresql").value == (dt.time(13, 50),) #Dates in a weird format for some reason

def test_17_set_end_time_value_postgresql(): #NOTE For some reason this doesn't recognise the key - Will look into it
        """A test to set the postgresql end time"""
        at = AppTest.from_file("db_bench.py").run()
        at.time_input(key="end_time_postgresql").set_value(dt.time(7, 30))
        assert at.date_input(key="end_time_postgresql").value == (dt.time(7, 30),) #Dates in a weird format for some reason

def test_18_submit_postgresql(): #NOTE For some reason this doesn't recognise the key - Will look into it
        """A test to click the submit button and start collecting postgresql data"""
        at = AppTest.from_file("db_bench.py").run()
        assert at.button(key="submit_postgresql").click().run()
        
def test_19_downsample_timescaledb_enable(): #TODO Implement downsample buttons
    """A test to check whether the downsample toggle can be clicked to enable it"""
    at = AppTest.from_file("db_bench.py").run()
    assert at.toggle(key="downsample_toggle_timescaledb").run()

def test_20_increment_downsample_value_clickhouse(): #NOTE For some reason this doesn't recognise the key - Will look into it
    """A test to increment the downsample number input"""
    at = AppTest.from_file("db_bench.py").run()
    at.number_input(key="downsample_value_clickhouse").increment().run()
    assert at.number_input(key="downsample_value_clickhouse").value == 1
        
def test_21_set_start_date_value_timescaledb():
        """A test to set the timescaledb start date"""
        at = AppTest.from_file("db_bench.py").run()
        at.date_input(key="start_date_timescaledb").set_value(dt.date(2024, 1, 1)).run()
        assert at.date_input(key="start_date_timescaledb").value == dt.date(2024, 1, 1)

def test_22_set_end_date_value_timescaledb():
        """A test to set the timescaledb end date"""
        at = AppTest.from_file("db_bench.py").run()
        at.date_input(key="end_date_timescaledb").set_value(dt.date(2019, 6, 6)).run()
        assert at.date_input(key="end_date_timescaledb").value == dt.date(2019, 6, 6)

def test_23_set_start_time_value_timescaledb(): #NOTE For some reason this doesn't recognise the key - Will look into it
        """A test to set the timescaledb start time"""
        at = AppTest.from_file("db_bench.py").run()
        at.time_input(key="start_time_timescaledb").set_value(dt.time(13, 50))
        assert at.date_input(key="start_time_timescaledb").value == (dt.time(13, 50),) #Dates in a weird format for some reason

def test_24_set_end_time_value_timescaledb(): #NOTE For some reason this doesn't recognise the key - Will look into it
        """A test to set the timescaledb end time"""
        at = AppTest.from_file("db_bench.py").run()
        at.time_input(key="end_time_timescaledb").set_value(dt.time(7, 30))
        assert at.date_input(key="end_time_timescaledb").value == (dt.time(7, 30),) #Dates in a weird format for some reason

def test_25_submit_timescaledb(): #NOTE For some reason this doesn't recognise the key - Will look into it
        """A test to click the submit button and start collecting timescaledb data"""
        at = AppTest.from_file("db_bench.py").run()
        assert at.button(key="submit_timescaledb").click().run()
