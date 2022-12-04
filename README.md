# README.md

## Getting started

To get started open this repository in vscode or github codespaces, it utilizes devcontainers to quickly get started.

To ingest the raw data ready for processing use the command:
`poetry run python -m pokemon.gather`

To process the data into the the form furfilling the requirements use the following command:
`poetry run python -m pokemon.process`

To start the streamlit dashboard, which operates on the parquet data from the above step.
`streamlit run pokemon/serve.py`

Additionally there are some test which can be run using `poetry run pytest tests/` (however note that I ran out of time to flesh these out)


## Architecture

### gather module

This module uses requests to execute a batch query to main pokedex api, which recieves list of all pokemon which are registered. This list is then used to ingest the detailed information for each pokemon, spark workers are used parallize this API scraping. An alternative better approach would be to use an asynchronous http library such as asyncio. The files are landed in their raw json format for further processing.

### process module

This module uses pyspark to filter and process the raw json files for each pokemon, it uses spark dataframe interface for the processing step, and was written such that the operations chained in a concise manner. The process module writes the output dataframe into an non-partitioned parquet file due to the extremely small filesize.


## Tasks

### Primary

- [x] Get list of all pokemon served by the API
- [x] Iterate through each pokemon, making an API call to retrieve the detailed json files
- [x] Process all pokemon files using pyspark to meet the primary requiremnts
- [x] Write data to appropriate format

### Bonus

- [x] Create dashboard to allow interactive visualization of data
- [x] Document how I would architect a continuous updating solution
- [x] Write description of GDPR approach
- [x] Implement solution using spark

## Thought process

- Informed that 2-4 hours would be suitable for this project, so implementation will be a POC using pyspark for local execution. Will document my thought process where taken assumptions/shortcuts given a lack of a databricks environment. However POC should be able to implemented in Databricks workspace with Kafka/Autoloader with minimal additional effort. The data volumes for this use-case is very low, so using spark was only to show my capabilities.

- Decided to download each file and process locally in a batch mode, in a cloud production environment I would consider use a databricks streaming based solution (kafka/autoloader/etc). Depending on the user of the solution I would also consider implemented as Delta Live Tables to make the pipeline easier for the end-user to maintain.

- Decided to scrape the main API for a list of all pokemon and use this list for iterating through each pokemon. I noted that there was also a generation API that I could've scraped for each of the requested (red, blue, leafgreen and white), however due to the small volume of data didn't see an advantage.

- Decided that a single parquet file would be a suitable format for this use-case due to the small dataset, current solution is batch based so overwrites the table on each execution.


### Bonus Requirement 1: GDPR

In order to handle such a case we should seperate personal identitifiable information into a secured lookup table, and use an artificial identifier (pseudonym) to link the working data to this lookup table. This means that we can simply remove the personal data in the lookup table in-order to comply with GDPR requests, whilst still having the working datasets available.

We can also use one-way cryptographic hashing with salting, which within Databricks means that if unauthorized users try to access the secret, they will see redacted values. However this adds some operational overhead with managing potentially multiple salts per user.

### Bonus Requirement 2: Continously updating

To build a system would continuously deliver updates, I would move towards using delta tables for storing the data, such that upserts would be simple to implement using the delta tables library. Delta tables also support change data feed, which allows easy tracking of changes to a delta table in a batch or streaming manner.

The data which is gathered from the API could be delivered via streaming manner (kafka/autoloader/etc), processed continuously or as microbatches, and deliver alerts / updates to the customer as they happen.

### Bonus Requirement 3: Interactive dashboard

Typically I would use PowerBI or make a SPA with vue for dashboarding, however I don't have a personal powerbi license, and a SPA would take too long as I would also have to develop a SPA. Therefore I chose to use streamlit as I had heard a lot about it and wanted to get a quick overview.