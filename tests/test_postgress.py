import datetime as dt
import pytest
from streamlit.testing.v1 import AppTest

def test_1_home_page_appears():
        """A test that will check the home page opens"""
        try:
                AppTest.from_file("../Home.py").run()
                assert True
        except:
                assert False

def test_2_downsample_clickhouse_enable():
    """A test to check whether the downsample toggle can be clicked to enable it"""
    at = AppTest.from_file("pages/ClickhouseDB.py").run()
    assert at.toggle(key="downsample_toggle_clickhouse").set_value(1).run()

def test_3_increment_downsample_value_clickhouse():
    """A test to increment the downsample number input"""
    at = AppTest.from_file("pages/ClickhouseDB.py").run()
    at.toggle(key="downsample_toggle_clickhouse").set_value(1).run()
    at.number_input(key="downsample_value_clickhouse").increment().run()
    assert at.number_input(key="downsample_value_clickhouse").value == 6 #Starts at 5

def test_4_set_downsample_value_clickhouse():
    """A test to increment the downsample number input"""
    at = AppTest.from_file("pages/ClickhouseDB.py").run()
    at.toggle(key="downsample_toggle_clickhouse").set_value(1).run()
    at.number_input(key="downsample_value_clickhouse").set_value(5000).run()
    assert at.number_input(key="downsample_value_clickhouse").value == 5000

def test_5_set_start_date_value_clickhouse():
        """A test to set the clickhouse start date"""
        at = AppTest.from_file("pages/ClickhouseDB.py").run()
        at.date_input(key="start_date_clickhouse").set_value(dt.date(2024, 1, 1)).run()
        assert at.date_input(key="start_date_clickhouse").value == dt.date(2024, 1, 1)

def test_6_set_end_date_value_clickhouse():
        """A test to set the clickhouse end date"""
        at = AppTest.from_file("pages/ClickhouseDB.py").run()
        at.date_input(key="end_date_clickhouse").set_value(dt.date(2019, 6, 6)).run()
        assert at.date_input(key="end_date_clickhouse").value == dt.date(2019, 6, 6)

def test_7_set_start_time_value_clickhouse():
        """A test to set the clickhouse start time"""
        at = AppTest.from_file("pages/ClickhouseDB.py").run()
        at.time_input(key="start_time_clickhouse").set_value(dt.time(13, 50))
        assert at.time_input(key="start_time_clickhouse").value == (dt.time(13, 50)) #Dates in a weird format for some reason

def test_8_set_end_time_value_clickhouse():
        """A test to set the clickhouse end time"""
        at = AppTest.from_file("pages/ClickhouseDB.py").run()
        at.time_input(key="end_time_clickhouse").set_value(dt.time(7, 30))
        assert at.time_input(key="end_time_clickhouse").value == (dt.time(7, 30)) #Dates in a weird format for some reason

@pytest.mark.xfail(reason=("Times out after 3 seconds due to data being imported"))
def test_9_submit_clickhouse():
        """A test to click the submit button and start collecting clickhouse data"""
        at = AppTest.from_file("pages/ClickhouseDB.py").run()
        assert at.button(key="submit_clickhouse").click().run()

def test_10_downsample_postgresql_enable():
    """A test to check whether the downsample toggle can be clicked to enable it"""
    at = AppTest.from_file("pages/PostgresqlDB.py").run()
    assert at.toggle(key="downsample_toggle_postgresql").set_value(1).run()

def test_11_increment_downsample_value_postgresql():
    """A test to increment the downsample number input"""
    at = AppTest.from_file("pages/PostgresqlDB.py").run()
    at.toggle(key="downsample_toggle_postgresql").set_value(1).run()
    at.number_input(key="downsample_value_postgresql").increment().run()
    assert at.number_input(key="downsample_value_postgresql").value == 6

def test_12_set_downsample_value_postgresql():
    """A test to increment the downsample number input"""
    at = AppTest.from_file("pages/PostgresqlDB.py").run()
    at.toggle(key="downsample_toggle_postgresql").set_value(1).run()
    at.number_input(key="downsample_value_postgresql").set_value(5000).run()
    assert at.number_input(key="downsample_value_postgresql").value == 5000
   
def test_13_set_start_date_value_postgresql():
        """A test to set the postgresql start date"""
        at = AppTest.from_file("pages/PostgresqlDB.py").run()
        at.date_input(key="start_date_postgresql").set_value(dt.date(2024, 1, 1)).run()
        assert at.date_input(key="start_date_postgresql").value == dt.date(2024, 1, 1)

def test_14_set_end_date_value_postgresql():
        """A test to set the postgresql end date"""
        at = AppTest.from_file("pages/PostgresqlDB.py").run()
        at.date_input(key="end_date_postgresql").set_value(dt.date(2019, 6, 6)).run()
        assert at.date_input(key="end_date_postgresql").value == dt.date(2019, 6, 6)

def test_15_set_start_time_value_postgresql():
        """A test to set the postgresql start time"""
        at = AppTest.from_file("pages/PostgresqlDB.py").run()
        at.time_input(key="start_time_postgresql").set_value(dt.time(13, 50))
        assert at.time_input(key="start_time_postgresql").value == (dt.time(13, 50))

def test_16_set_end_time_value_postgresql():
        """A test to set the postgresql end time"""
        at = AppTest.from_file("pages/PostgresqlDB.py").run()
        at.time_input(key="end_time_postgresql").set_value(dt.time(7, 30))
        assert at.time_input(key="end_time_postgresql").value == (dt.time(7, 30)) 

@pytest.mark.xfail(reason=("Times out after 3 seconds due to data being imported"))
def test_17_submit_postgresql():
        """A test to click the submit button and start collecting postgresql data"""
        at = AppTest.from_file("pages/PostgresqlDB.py").run()
        assert at.button(key="submit_postgresql").click().run()
        
def test_18_downsample_timescaledb_enable():
    """A test to check whether the downsample toggle can be clicked to enable it"""
    at = AppTest.from_file("pages/TimescaleDB.py").run()
    assert at.toggle(key="downsample_toggle_timescaledb").set_value(1).run()

def test_19_increment_downsample_value_timescaledb():
    """A test to increment the downsample number input"""
    at = AppTest.from_file("pages/TimescaleDB.py").run()
    at.toggle(key="downsample_toggle_timescaledb").set_value(1).run()
    at.number_input(key="downsample_value_timescaledb").increment().run()
    assert at.number_input(key="downsample_value_timescaledb").value == 6

def test_20_set_downsample_value_timescaledb():
    """A test to increment the downsample number input"""
    at = AppTest.from_file("pages/TimescaleDB.py").run()
    at.toggle(key="downsample_toggle_timescaledb").set_value(1).run()
    at.number_input(key="downsample_value_timescaledb").set_value(5000).run()
    assert at.number_input(key="downsample_value_timescaledb").value == 5000
        
def test_21_set_start_date_value_timescaledb():
        """A test to set the timescaledb start date"""
        at = AppTest.from_file("pages/TimescaleDB.py").run()
        at.date_input(key="start_date_timescaledb").set_value(dt.date(2024, 1, 1)).run()
        assert at.date_input(key="start_date_timescaledb").value == dt.date(2024, 1, 1)

def test_22_set_end_date_value_timescaledb():
        """A test to set the timescaledb end date"""
        at = AppTest.from_file("pages/TimescaleDB.py").run()
        at.date_input(key="end_date_timescaledb").set_value(dt.date(2019, 6, 6)).run()
        assert at.date_input(key="end_date_timescaledb").value == dt.date(2019, 6, 6)

def test_23_set_start_time_value_timescaledb():
        """A test to set the timescaledb start time"""
        at = AppTest.from_file("pages/TimescaleDB.py").run()
        at.time_input(key="start_time_timescaledb").set_value(dt.time(13, 50))
        assert at.time_input(key="start_time_timescaledb").value == (dt.time(13, 50))

def test_24_set_end_time_value_timescaledb():
        """A test to set the timescaledb end time"""
        at = AppTest.from_file("pages/TimescaleDB.py").run()
        at.time_input(key="end_time_timescaledb").set_value(dt.time(7, 30))
        assert at.time_input(key="end_time_timescaledb").value == (dt.time(7, 30))

def test_25_submit_timescaledb():
        """A test to click the submit button and start collecting timescaledb data"""
        at = AppTest.from_file("pages/TimescaleDB.py").run()
        assert at.button(key="submit_timescaledb").click().run()

# def test_26_downsample_arcticdb_enable():
#     """A test to check whether the downsample toggle can be clicked to enable it"""
#     at = AppTest.from_file("pages/ArcticDB.py").run()
#     assert at.toggle(key="downsample_toggle_arcticdb").set_value(1).run()

def test_27_increment_downsample_value_arcticdb():
    """A test to increment the downsample number input"""
    at = AppTest.from_file("pages/ArcticDB.py").run()
    at.toggle(key="downsample_toggle_arcticdb").set_value(1).run()
    at.number_input(key="downsample_value_arcticdb").increment().run()
    assert at.number_input(key="downsample_value_arcticdb").value == 6

def test_28_set_downsample_value_arcticdb():
    """A test to increment the downsample number input"""
    at = AppTest.from_file("pages/ArcticDB.py").run()
    at.toggle(key="downsample_toggle_arcticdb").set_value(1).run()
    at.number_input(key="downsample_value_arcticdb").set_value(5000).run()
    assert at.number_input(key="downsample_value_arcticdb").value == 5000
        
def test_29_set_start_date_value_arcticdb():
        """A test to set the arcticdb start date"""
        at = AppTest.from_file("pages/ArcticDB.py").run()
        at.date_input(key="start_date_arcticdb").set_value(dt.date(2024, 1, 1)).run()
        assert at.date_input(key="start_date_arcticdb").value == dt.date(2024, 1, 1)

def test_30_set_end_date_value_arcticdb():
        """A test to set the arcticdb end date"""
        at = AppTest.from_file("pages/ArcticDB.py").run()
        at.date_input(key="end_date_arcticdb").set_value(dt.date(2019, 6, 6)).run()
        assert at.date_input(key="end_date_arcticdb").value == dt.date(2019, 6, 6)

def test_31_set_start_time_value_arcticdb():
        """A test to set the arcticdb start time"""
        at = AppTest.from_file("pages/ArcticDB.py").run()
        at.time_input(key="start_time_arcticdb").set_value(dt.time(13, 50))
        assert at.time_input(key="start_time_arcticdb").value == (dt.time(13, 50))

def test_32_set_end_time_value_arcticdb():
        """A test to set the arcticdb end time"""
        at = AppTest.from_file("pages/ArcticDB.py").run()
        at.time_input(key="end_time_arcticdb").set_value(dt.time(7, 30))
        assert at.time_input(key="end_time_arcticdb").value == (dt.time(7, 30))

@pytest.mark.xfail(reason=("Times out after 3 seconds due to data being imported"))
def test_33_submit_arcticdb():
        """A test to click the submit button and start collecting timescaledb data"""
        at = AppTest.from_file("pages/ArcticDB.py").run()
        assert at.button(key="submit_arcticdb").click().run()

@pytest.mark.xfail(reason=("Times out after 3 seconds due to data being imported"))
def test_34_edit_all_values_clickhouse():
        """A test to change all the controlable values for the chosen DB then check they are the same when Submit button selected"""
        at = AppTest.from_file("pages/ClickhouseDB.py").run()
        at.toggle(key="downsample_toggle_clickhouse").set_value(1).run()
        at.number_input(key="downsample_value_clickhouse").set_value(5000).run()
        at.date_input(key="start_date_clickhouse").set_value(dt.date(2021, 9, 8)).run()
        at.date_input(key="end_date_clickhouse").set_value(dt.date(2022, 6, 6)).run()
        at.time_input(key="start_time_clickhouse").set_value(dt.time(11, 35))
        at.time_input(key="end_time_clickhouse").set_value(dt.time(14, 00))
        at.button(key="submit_clickhouse").click().run()
        
        if at.number_input(key="downsample_value_clickhouse").value == 5000 and at.date_input(key="start_date_clickhouse").value == dt.date(2021, 9, 8) and at.date_input(key="end_date_clickhouse").value == dt.date(2022, 6, 6) \
                and at.time_input(key="start_time_clickhouse").value == (dt.time(11, 35)) and at.time_input(key="end_time_clickhouse").value == (dt.time(14, 00)):
               assert True
        else:
               assert False

@pytest.mark.xfail(reason=("Times out after 3 seconds due to data being imported"))
def test_35_edit_all_values_postgresql():
        """A test to change all the controlable values for the chosen DB then check they are the same when Submit button selected"""
        at = AppTest.from_file("pages/PostgresqlDB.py").run()
        at.toggle(key="downsample_toggle_postgresql").set_value(1).run()
        at.number_input(key="downsample_value_postgresql").set_value(5000).run()
        at.date_input(key="start_date_postgresql").set_value(dt.date(2021, 9, 8)).run()
        at.date_input(key="end_date_postgresql").set_value(dt.date(2022, 6, 6)).run()
        at.time_input(key="start_time_postgresql").set_value(dt.time(11, 35))
        at.time_input(key="end_time_postgresql").set_value(dt.time(14, 00))
        at.button(key="submit_postgresql").click().run()

        if at.number_input(key="downsample_value_postgresql").value == 5000 and at.date_input(key="start_date_postgresql").value == dt.date(2021, 9, 8) and at.date_input(key="end_date_postgresql").value == dt.date(2022, 6, 6) \
                and at.time_input(key="start_time_postgresql").value == (dt.time(11, 35)) and at.time_input(key="end_time_postgresql").value == (dt.time(14, 00)):
                assert True
        else:
                assert False

def test_36_edit_all_values_timescaledb():
        """A test to change all the controlable values for the chosen DB then check they are the same when Submit button selected"""
        at = AppTest.from_file("pages/TimescaleDB.py").run()
        at.toggle(key="downsample_toggle_timescaledb").set_value(1).run()
        at.number_input(key="downsample_value_timescaledb").set_value(5000).run()
        at.date_input(key="start_date_timescaledb").set_value(dt.date(2021, 9, 8)).run()
        at.date_input(key="end_date_timescaledb").set_value(dt.date(2022, 6, 6)).run()
        at.time_input(key="start_time_timescaledb").set_value(dt.time(11, 35))
        at.time_input(key="end_time_timescaledb").set_value(dt.time(14, 00))
        at.button(key="submit_timescaledb").click().run()

        if at.number_input(key="downsample_value_timescaledb").value == 5000 and at.date_input(key="start_date_timescaledb").value == dt.date(2021, 9, 8) and at.date_input(key="end_date_timescaledb").value == dt.date(2022, 6, 6) \
                and at.time_input(key="start_time_timescaledb").value == (dt.time(11, 35)) and at.time_input(key="end_time_timescaledb").value == (dt.time(14, 00)):
                assert True
        else:
                assert False

@pytest.mark.xfail(reason=("Times out after 3 seconds due to data being imported"))
def test_37_edit_all_values_arcticdb():
        """A test to change all the controlable values for the chosen DB then check they are the same when Submit button selected"""
        at = AppTest.from_file("pages/ArcticDB.py").run()
        at.toggle(key="downsample_toggle_arcticdb").set_value(1).run()
        at.number_input(key="downsample_value_arcticdb").set_value(5000).run()
        at.date_input(key="start_date_arcticdb").set_value(dt.date(2021, 9, 8)).run()
        at.date_input(key="end_date_arcticdb").set_value(dt.date(2022, 6, 6)).run()
        at.time_input(key="start_time_arcticdb").set_value(dt.time(11, 35))
        at.time_input(key="end_time_arcticdb").set_value(dt.time(14, 00))
        at.button(key="submit_arcticdb").click().run()

        if at.number_input(key="downsample_value_arcticdb").value == 5000 and at.date_input(key="start_date_arcticdb").value == dt.date(2021, 9, 8) and at.date_input(key="end_date_arcticdb").value == dt.date(2022, 6, 6) \
                and at.time_input(key="start_time_arcticdb").value == (dt.time(11, 35)) and at.time_input(key="end_time_arcticdb").value == (dt.time(14, 00)):
                assert True
        else:
                assert False
