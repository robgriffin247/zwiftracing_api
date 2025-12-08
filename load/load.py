import duckdb
from extract.endpoints import get_event
import time
from datetime import datetime

ids = [5188741, 5200082]

for id in ids:

    with duckdb.connect("load/data/analytics.duckdb") as con:

        print("Creating raw schema")
        con.sql("CREATE SCHEMA IF NOT EXISTS raw")

        print("Creaing tables")
        con.sql("CREATE TABLE IF NOT EXISTS raw.events (event_id BIGINT, event_time BIGINT, route_id BIGINT, event_distance FLOAT, load_timestamp BIGINT)")
        con.sql("CREATE TABLE IF NOT EXISTS raw.results (event_id BIGINT, rider_id BIGINT, rider VARCHAR, velo_90 FLOAT, race_time FLOAT, load_timestamp BIGINT)")


        print(f"Getting event {id}")
        load_timestamp = int(datetime.now().timestamp()*1000)
        event = get_event(id)

        results = event.get("results")

        print("Populating events table")
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
        
        print("Populating results table")
        i = 0
        for r in results:

            i += 1
            if i%10==0:
                print(f"{i} of {len(results)} results loaded...")

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

    if id!=ids[-1]:
        print("Waiting...")
        time.sleep(61) # 61 second timeout if not final event to load, to protect API
    else:
        print("Complete!")

