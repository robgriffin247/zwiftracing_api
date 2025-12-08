# Using the ZwiftRacing API with Python

<!-- 
# Demo 0: Setting up a development environment in Windows

- WSL2
- uv
- direnv
-->

## Demo 1: Extract from ZRAPP

This contains basic usage of all zwiftracing.app API endpoints allowing users ton extract from the data source. 
Each endpoint has a ready-to-use function that takes an ID/list of IDs for the rider(s), club or event of interest as an input and returns the data as a Python object (a dictionary or list of dictionaries depending on the endpoint).
 
See the associated [README](extract/README.md) file for details, [endpoints.py](extract/endpoints.py) for each function and [data/](extract/data/) for examples of outputs.

## Coming soon...

- setting up a dev environment
- duckdb/motherduck; incl. notebooks/UI
- dlt
- dbt
- streamlit
