# Database TestBench

This is a public repo used for collaboration on a student project between Solent University and Rockstone Data Ltd.

## Problem Statement
The number of different database technologies is expandin. Becoming more specialized to particular applications, with associated potential performance boosts (eg OLTP vs OLAP) and cost savings.

At Rockstone Data we have utilized a relatively new [column orientated database](https://atlan.com/what-is/columnar-database/) called ClickhouseDB to host very large time series data tables (700m+ rows). This class of database was first described in [‘C-Store: A Column-orientated DBMS’](https://people.brandeis.edu/~nga/papers/VLDB05.pdf) and outperforms traditional row orientated databases in both speed and storage.

The project aim is to create an interactive demonstrator running on the company website clearly demonstrating these benefits vs ‘traditional’ or row-orientated databases.

## Solution Overview 
Create a one page ‘dashboard’ web app which has a line plot of a scalar value over time, a start / end datetime picker and a database source picker.
The database source options will be one of postgres, postgres + timescaleDB or ClickhouseDB. 

There will be submit button that when pressed fetches the data for the plot.
There will also be a ‘downsampling on-off’ toggle. And a [downsampling](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference/largestTriangleThreeBuckets) count text entry.

On pressing ‘submit’ a timer is started that times how long it takes to fetch the data (note this will not include the time taken for the charting library to load it). 

The elapsed time will be displayed on the dashboard near the line chart. Text boxes will be populated showing the space taken up on disk for the table, and the number of rows in the table. A text box showing GB of disk storage per million rows will be shown.

## Tech Stack Requirements
The project will be built using Python Plotly Dash. Development will use Python venv and pip to ensure a machine independent virtual environment. VS Code will be used for the IDE with step by step debug. 

For local development the databases will be run inside Docker containers, with one for postgres, two (chs and chc) for Clickhouse and, as required another for postgres + Timescale (the author is unfamiliar with TimescaleDB so looks to the student to advise). 

Docker-compose will be used in deployment and for local start/stopping of the databases.

Test data will need to be created on eg a once/second basis for 1 to 100 years. Ideally something with variations that are visible on a 24 hour, monthly and yearly plot. Advice can be provided on the best way to do this. Test data is only created once before deployment.

## Stretch Goals 
Identify a class of data that can be plotted as eg a geo-heatmap or spectrograph or surface plot (ie more dimensions), maybe with animations or orientation controls. Generate the data and add the plot (map or other) below the line chart.

Benchmark Mongo DB timeseries collections.
Compare costs with Snowflake/Data Dog etc see X post [here](https://x.com/PierreDeWulf/status/1745464855723986989?s=20)
Benchmark writing data to the large tables. 

## Way of Working
Rockstone Data has created this public repo along with a ‘Project’ view onto which the student will curate a backlog of ‘Issues’, moving them across the board Kanban style as they progress. The student will be expected to use ‘Issue comments’ as a form of log-book to facilitate communications. This is known as ['Feature Branch Workflow'](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow) or ['Git Flow'](https://blog.hubspot.com/website/github-flow). A high level of autonomy and problem-solving initiative will be required.

The GitHub development flow will be used where individuals create a branch for issues they are working on. The branch will be named eg:
nt_123_short_desc
So 'nt' is the developer's initials, 123 is the Issue Number followed by a one or two word description of the Issue.
We will try to adhere to the 'Joel Test' of good software practice.

## Documentation
We will create a docs directory and make notes in Markdown to share knowledge across the team. If we need to add screenshots, then place them in a GitHub Discussions post and link to the docs entry.

## Teamwork
A good team cosists of everyone trying to help eachother, the leader is there as a coach and to maximise productivity of the team, finding and removing blockers.

## Useful Links
| Description | Link |
| -- | -- |
| Quick ands simple test of the quality of your software team | https://blog.hubspot.com/service/joel-test |
| Python plotly chart plotting library | https://plotly.com/examples/ |
| Quick guide to using Virtual Environemnts to speed Python dev | https://realpython.com/python-virtual-environments-a-primer/ |
| What is clickhouse DB ? | https://clickhouse.com/docs/en/intro#:~:text=ClickHouse%C2%AE%20is%20a%20high,software%20and%20a%20cloud%20offering. |
| Postgres DB docs| https://www.postgresql.org/ |
| Timescale the time series add-on for Postgres |https://www.timescale.com/ |
| Guide to using Docker Compose |  https://docs.docker.com/get-started/08_using_compose/
| How-To manage projects in Github (See Project Management section) | https://docs.github.com/en |
| The original Column Orientated DB paper| https://people.brandeis.edu/~nga/papers/VLDB05.pdf |
| Python in Visual Studio Code | https://code.visualstudio.com/docs/languages/python |
| A minimal Plotly Dash App | https://dash.plotly.com/minimal-app |
| Downsampling in Clickhouse | https://clickhouse.com/videos/downsampling-time-series-data-with-plot-ly-and-ClickHouse |
| Largest Triangle Three Buckets | https://clickhouse.com/blog/clickhouse-release-23-10 |
 
# Installing and Using this Repo

This project has four main componenents initially, 
1. the Flask/Plotly/Dash python module.
2. the Postgres Docker container
3. the two Clickhouse DB containers

The steps to install and run it are:

Git clone this repo then create the virtual environment and install the packages:

```
cd db_bench
python -m venv .venv
pip install -r requirements.txt
```

Create local versions of the config files
```
cp .vscode/launch_example.json .vscode/launch.json
cp .env_example .env
cp postgres.env_example postgres.env
```

This will create a subdirectory ```.venv``` containing a virtual Python environment isolating the project from other projects on your computer. You may want to move across to using the poetry package manager as one of your deliverables. It handles dependencies in a more intelligent way than venv and pip.

If you're using VS Code, note the .vscode directory which contains an entry allowing you to [start and debug](https://code.visualstudio.com/docs/languages/python#_debugging) the project.

You can try this now, but will likely get errors about not being able to connect to the database. So the next step is to run up the Docker containers for Clickhouse and configure them. You will need [Docker Desktop installed](https://docs.docker.com/desktop/install/mac-install/) on your machine. 

```
cd db_bench
docker-compose up ch_server ch_client
```
This will build your contaienrs and run them locally. You can see their status with ``` docker container ls -a```.

Now we need to check that the clickhouse database is running locally, choose your preferred SQL client. I like to use [DBeaver](https://dbeaver.io/download/). Create a connection of type Clickhouse on localhost, port ``` 8123  ``` (specified in docker-compose.yml), user ``` chuser ``` and password ```chuser_pwd ```  (specified in /etc/clickhouse-server/users.d/chuser.xml and .env) and we start with database ``` default ```.

You should now be able to connect to your locally running Clickhouse docker container. When you are connected, open an SQL terminal and create the database.

``` 
CREATE DATABASE ts_db;
```

Now create the demo timeseries table with the following SQL command. This only creates a small table. Once you're sure of the installation, change all the ```toDate(2021``` to ```toDate(2022``` to generate a year and 10 minute's worth of 1 second time series data.

```
CREATE TABLE demo_ts 
ENGINE = MergeTree
ORDER BY tuple()
AS
SELECT toDateTime(arrayJoin(range(toUInt32(toDateTime('2021-01-01 00:00:00')), toUInt32(toDateTime('2021-01-01 00:10:00')), 1) )) as cdatetime,
       toSecond(toDateTime(arrayJoin(range(toUInt32(toDateTime('2021-01-01 00:00:00')), toUInt32(toDateTime('2021-01-01 00:10:00')), 1) ))) +
       toMinute(toDateTime(arrayJoin(range(toUInt32(toDateTime('2021-01-01 00:00:00')), toUInt32(toDateTime('2021-01-01 00:10:00')), 1) ))) +
       2 * toHour(toDateTime(arrayJoin(range(toUInt32(toDateTime('2021-01-01 00:00:00')), toUInt32(toDateTime('2021-01-01 00:10:00')), 1) ))) +
       5 * toDayOfWeek(toDateTime(arrayJoin(range(toUInt32(toDateTime('2021-01-01 00:00:00')), toUInt32(toDateTime('2021-01-01 00:10:00')), 1) ))) +
       8 * toWeek(toDateTime(arrayJoin(range(toUInt32(toDateTime('2021-01-01 00:00:00')), toUInt32(toDateTime('2021-01-01 00:10:00')), 1) ))) +
       12 * toMonth(toDateTime(arrayJoin(range(toUInt32(toDateTime('2021-01-01 00:00:00')), toUInt32(toDateTime('2021-01-01 00:10:00')), 1) ))) +
       20 * (toYear(toDateTime(arrayJoin(range(toUInt32(toDateTime('2021-01-01 00:00:00')), toUInt32(toDateTime('2021-01-01 00:10:00')), 1) )))-2021) as ts_values
```

Now you can restart the chdemoapp.py app and it should connect to the clickhouse database and show some data.

Note the Dockerfile is unused, but can be used at a later date for deployment as a Docker container, alongside the appropriate service in docker-compose.yml.

# Very Initial Draft Example Screenshot of GUI

![Early Draft Example](https://github.com/NickThorne123/db_bench/assets/115091926/e9310617-cec2-46a1-bc32-f8f1c8a9326f)
