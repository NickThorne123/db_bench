import datetime as dt
from streamlit.testing.v1 import AppTest

def test_downsample_postgres_enable():
    """A test to check whether the downsample toggle can be clicked to enable it"""
    at = AppTest.from_file("db_bench.py").run()
    assert at.toggle(key="downsample_toggle_postgres").run()

def test_aggregate_postgres_enable():
    """A test to check whether the aggregate toggle can be clicked to enable it"""
    at = AppTest.from_file("db_bench.py").run()
    assert at.toggle(key="aggregate_toggle_postgres").run()

# def test_increment_downsample_value_postgres(): #NOTE For some reason this doesn't recognise the key - Will look into it
#     """A test to increment the downsample number input"""
#     at = AppTest.from_file("db_bench.py").run()
#     at.number_input(key="downsample_value_postgres").increment().run()
#     assert at.number_input(key="downsample_value_postgres").value == 1

# def test_check_radio_values_postgres(): #NOTE For some reason this doesn't recognise the key - Will look into it
#     """A test to check the default values of the radio buttons"""
#     at = AppTest.from_file("db_bench.py").run()
#     at.radio(key="postgres_downsample_time").set_value("Seconds").run()
#     assert at.radio(key="postgres_downsample_time").options["Seconds", "Minutes", "Hours", "Days", "Weeks", "Months", "Years"]

def test_set_start_date_value_postgres():
        """A test to set the postgres start date"""
        at = AppTest.from_file("db_bench.py").run()
        at.date_input(key="start_date_postgres").set_value(dt.date(2024, 1, 1)).run()
        assert at.date_input(key="start_date_postgres").value == dt.date(2024, 1, 1)

def test_set_end_date_value_postgres():
        """A test to set the postgres end date"""
        at = AppTest.from_file("db_bench.py").run()
        at.date_input(key="end_date_postgres").set_value(dt.date(2019, 6, 6)).run()
        assert at.date_input(key="end_date_postgres").value == dt.date(2019, 6, 6)

# def test_set_start_time_value_postgres(): #NOTE For some reason this doesn't recognise the key - Will look into it
#        """A test to set the postgres start time"""
#         at = AppTest.from_file("db_bench.py").run()
#         at.time_input(key="start_time_postgres").set_value(dt.time(13, 50))
#         assert at.date_input(key="start_time_postgres").value == (dt.time(13, 50),) #Dates in a weird format for some reason

# def test_set_end_time_value_postgres(): #NOTE For some reason this doesn't recognise the key - Will look into it
#        """A test to set the postgres end time"""
#         at = AppTest.from_file("db_bench.py").run()
#         at.time_input(key="end_time_postgres").set_value(dt.time(7, 30))
#         assert at.date_input(key="end_time_postgres").value == (dt.time(7, 30),) #Dates in a weird format for some reason