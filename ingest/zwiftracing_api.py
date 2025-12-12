from extract.endpoints import get_event
import dlt
import os
import httpx
import json




@dlt.resource(
    name="events", 
    write_disposition="merge",
    primary_key="eventId",
)
def fetch_event(id):
    event = get_event(id)
    
    """
    Variant columns can occur in dlt; e.g. gap in the first result is 0, an integer, while subsequent values are a float
    dlt will set the schema from the first row; gap becomes an int
    when it meets the second row, it finds a float which is incompatible with the schema, so makes the column gap__v_double
    This can be handled by typing on ingestion, or left in the raw data and handled dowenstream
    I prefer want to prevent this as downstream handling relies on the column being present which can be clunky if using multiple databases (dev and prod)
    """
    results = event.get("results")
    
    for r in results:
        gap = r.get("gap")
        r["gap"] = float(gap) if gap else None

    event["results"] = results


    yield event

def ingest_event(id):
    _destination =dlt.destinations.duckdb(
        credentials="ingest/data/zwiftracing_api_demo_ingest.duckdb"
    )

    pipeline = dlt.pipeline(
        pipeline_name=f"zwiftracing_api_demo_ingest_pipeline",
        destination=_destination,
        dataset_name="zwiftracing_api",
    )

    load_info = pipeline.run(fetch_event(id))

    return load_info



if __name__=="__main__":
    
    ingest_event(5188741)
