from arcticdb import Arctic
import os
from clickhouse_driver import Client
from pandas import DataFrame
from dotenv import load_dotenv

load_dotenv(override=True)

ARCTIC_URL=os.getenv('ARCTIC_URL')
CH_HOST=os.getenv('CH_HOST')
CH_PORT=os.getenv('CH_PORT')
CH_PASSWORD=os.getenv('CH_PASSWORD')
CH_USER=os.getenv('CH_USER')
CH_DBNAME=os.getenv('CH_DBNAME')

client = Client(host=CH_HOST, port=CH_PORT, settings={'use_numpy': True}, user=CH_USER, password=CH_PASSWORD)

try:
    ac = Arctic(uri=ARCTIC_URL)
    ac.create_library("demo_ts")

    clickhouse_data_query =  f""" SELECT * from ts_db.demo_ts """
    clickhouse_data = client.execute(clickhouse_data_query, settings={'use_numpy': True})
    df = DataFrame(clickhouse_data)

    db_bench_lib = ac["demo_ts"]
    db_bench_lib.write("demo_ts_frame", df)
    print("Data successfully sent to S3 Bucket!")
except Exception:
    print("Something went wrong! Make sure the Clickhouse DB server is running and check the public facing permissions in AWS")
