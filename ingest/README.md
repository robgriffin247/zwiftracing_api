# Demo: Ingest with dlt

The dlt tool can make the ingestion of data &mdash; especially large, complex and nested json structures &mdash; *very* simple. Compare [``load.py``](../load/load.py) which loads two small and simple tables to a DuckDB database, to [``zwiftracing_api.py``](zwiftracing_api.py). The code in ``load.py`` is far more complicated and involves a lot more hard-coding than in the dlt equivalent. Even the code in the dlt example is unneccessarily long and inflexible as it contains hard-coded typing, which isn't needed but is there to serve as an example of how to solve variant columns &mdash; you could reduce ``fetch_event()`` to  

```
def fetch_event(id):
    yield get_event(id)
```


#### Ingest

```
uv run ingest/zwiftracing_app.py
duckdb
```

In duckdb

```
attach 'ingest/data/zwiftracing_api_demo_ingest.duckdb';
show all tables;
describe table zwiftracing_api_demo_ingest.zwiftracing_api.events__results;
select * from zwiftracing_api_demo_ingest.zwiftracing_api.events;
select * from zwiftracing_api_demo_ingest.zwiftracing_api.events__results;
.exit;
```