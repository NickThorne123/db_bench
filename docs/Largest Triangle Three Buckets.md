### Overview

LTTB is a down sampling technique done by dividing the sorted series into buckets and then finding the largest triangle in each bucket. 

Down sampling is the process of transforming data, reducing its resolution so that it requires less space, while preserving some of its basic characteristics so that it is still usable.

### How it is imported

This is imported into the application via the Clickhouse library. There are multiple different ways of importing it but the way that is used in the chdemoapp [Demo App](https://github.com/NickThorne123/db_bench/blob/master/chdemoapp.py) on the repo, by using the following statement:

``` from clickhouse_driver import Client ```

This then allows us to import the necessary modules to make use of the LTTB.

### How it used in code

To use this in code, first we must define the client, within the demo app above currently stored in the repo this is completed through a function called get_ch_client and is called within the update_output function by setting it equal too a variable called client:

``` 
def get_ch_client():
    """
    Create a Clickhouse DB client object (aka connection)
    """
    client = Client(host=CH_HOST, port=CH_PORT, settings={'use_numpy': True}, user=CH_USER, password=CH_PASSWORD)
    return client

```

This is then ingested into a SQL query, inputting the data into LTTB function and by defining the values for how many points you want, pass in the x which is the time and the y which is the number of values available in the time series data.

```
downsample_query = f""" from ts_db.demo_ts select untuple(arrayJoin(largestTriangleThreeBuckets({std_window})(cdatetime, ts_values )))
                   where toDateTime(cdatetime) >= toDateTime('{start_date_str}') and toDateTime(cdatetime) <= toDateTime('{to_date_str}') """
```

As you can see the LTTB function largestTriangleThreeBuckets(n)(x, y) takes 1 parameter and 3 arguments.

`N (parameter)` - Is the number of points in the resulting series and in this is set to `std_window` 

`X (1st Argument)` - Is the time span you want the down sampled graph to use

`Y (2nd Argument)` - Is the number of values in the time series data you want to reduce

The query is then put into a variable named res_list_agg and printed out in a graph.

```
res_list_agg = client.execute(downsample_query, settings={'use_numpy': True})
        elapsed = time.time() - start_t
        df_agg = pd.DataFrame(res_list_agg, columns =['cdatetime','ts_values'])
        fig_agg_row_count = df_agg.shape[0]
        fig_agg = px.line(df_agg, x='cdatetime', y='ts_values') 
        fig_agg.update_layout(title_text = f"Downsampled Chart ({fig_agg_row_count}/{std_window} of {res_count:,} rows) query time:{elapsed:0.2f}s", title_x=0.5, xaxis_title='Date and Time', yaxis_title = 'Downsampled Value')
```

### Useful Links

[LTTB Clickhouse Documentation](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference/largestTriangleThreeBuckets)

[Video on how to use basic LTTB](https://clickhouse.com/videos/downsampling-time-series-data-with-plot-ly-and-ClickHouse)
