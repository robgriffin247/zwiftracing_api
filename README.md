# Using the ZwiftRacing API with Python

<!-- 
# Demo 0: Setting up a development environment in Windows

- WSL2
- uv
- direnv
-->

## Demo 1: Extract from ZRAPP

This [demo](extract/) contains basic usage of all zwiftracing.app API endpoints allowing users ton extract from the data source. 
Each endpoint has a ready-to-use function that takes an ID/list of IDs for the rider(s), club or event of interest as an input and returns the data as a Python object (a dictionary or list of dictionaries depending on the endpoint).


## Demo 2: Load data to DuckDB

This [demo](load/) contains a basic demo of loading data from a ZwiftRacing.app API endpoint into a pair of DuckDB tables in a database, along with some intstruction on basic SQL code to explore data.


## Demo 3: Ingest with dlt

This [demo](ingest/) contains an example of loading data to DuckDB using dlt, a tool to make loading complex data sources to databases extremely simple.

## Coming soon...

- setting up a dev environment
- dbt
- streamlit


<!-- Motherduck? and TARGET -->