# Demo 2: Load to DuckDB

**Aim:** Load data from a Python object, extracted from the ZwiftRacing.app API, and load it to a DuckDB database.

## Prerequisites

- Development environment
- ZwiftRacing.app API key
- Duckdb; this will be used for the database. It is a fast, powerful and open-source database system. Duckdb can store data locally or in the cloud using a free MotherDuck account &mdash; integration between the two is seamless, making it easy to develop and test locally before deploying changes to cloud-based data in production. Add duckdb to the project:

    ``uv add duckdb``

- An understanding of how to load and manipulate the data in Python (see [extract demo](../extract/))

## Exmaple project

The demo will show how to make a pair of tables, as could be used to create standings in a race series etc. The tables will be:
- ``events`` which contains one row per event, with ``event_id``, the start ``event_time``, the ``route_id`` and the ``event_distance``
- ``results`` which contains one row per finisher in each event, with ``event_id``, ``rider_id``, ``rider``, 90-day max vELO rating (``velo_90``) and ``race_time``

Data will come from two events ([``5188741``](https://zwiftpower.com/events.php?zid=5188741), [``5200082``](https://zwiftpower.com/events.php?zid=5200082)) in the Cycling Time-Trials Winter Series 2025/26.

## Load to DuckDB

For the full code, see [the script](load.py), but here I show the important snippets.

1. Create the database, schema and tables (if needed); ``analytics.duckdb`` is the database, ``raw`` is the schema and ``events`` and ``results`` are the tables. The schema of the tables (yes, another sort of schema - it's confusing language there) are defined on creation.

    ```    
    with duckdb.connect("load/data/analytics.duckdb") as con:

        print("Creating raw schema")
        con.sql("CREATE SCHEMA IF NOT EXISTS raw")

        print("Creaing tables")
        con.sql("CREATE TABLE IF NOT EXISTS raw.events (event_id BIGINT, event_time BIGINT, route_id BIGINT, event_distance FLOAT, load_timestamp BIGINT)")
        con.sql("CREATE TABLE IF NOT EXISTS raw.results (event_id BIGINT, rider_id BIGINT, rider VARCHAR, velo_90 FLOAT, race_time FLOAT, load_timestamp BIGINT)")
    ```

1. Get the data from the endpoint

1. Populate the data into the tables with a parameterised load (``?`` and ``[èvent.get("eventID"), ...]``)

    ```
    con.execute("""
        INSERT INTO raw.events 
        SELECT ? as event_id, 
            ? as event_time, 
            ? as route_id, 
            ? as event_distance,
            ? as load_timestamp
        """, 
        [event.get('eventId'), event.get('time'), event.get('routeId'), event.get('distance'), load_timestamp]
    )

    for r in results:
        con.execute("""
            INSERT INTO raw.results 
            SELECT ? as event_id, 
                ? as rider_id, 
                ? as rider, 
                ? as velo_90,
                ? as race_time,
                ? as load_timestamp
            """,
            [event.get('eventId'), r.get('riderId'), r.get('name'), 
            r.get('ratingMax90'), r.get('time'), load_timestamp]
        )
    ```

## Explore data in DuckDB

Once the data is in the database, you can view, modify and use the data using DuckDB. You can either do that in the command line or using the UI. 
To view in the command line, execute ``duckdb``. To view in the UI, run ``duckdb -ui``, then follow the link (you may need to install the duckdb ui, depending on the version you have &mdash; follow the prompts). You will need to attach the database, then you can ues ``select`` statements to explore the data. SQL is a fairly simple language to get started with, so go explore, but here are some examples!

```
-- Attach the database to the session
attach 'data/analytics.duckdb';

-- View the raw events table
select * 
from analytics.raw.events;

-- View the raw results table
select * 
from analytics.raw.results;

-- View the riders in order of event and race_time (fastest first)
select rider, race_time 
from analytics.raw.results 
order by event_id, race_time desc;

-- View the rider ids with a velo_90 >=2000
select rider_id 
from analytics.raw.results 
where velo_90>=2000 
group by rider_id;

-- Merge distance on to results and get speed, and filtering to those >35 km/h
select 
    results.*, 
    events.event_distance / (results.race_time/3600) as race_speed 
from analytics.raw.results 
    left join analytics.raw.events using(event_id);
```
