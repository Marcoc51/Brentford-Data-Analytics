import dlt
from dlt.sources.sql_database import sql_database

# Define the PostgreSQL Database resource
def load_entire_database() -> None:
    # Define the pipeline
    pipeline = dlt.pipeline(
        pipeline_name="extract_postgres_database",
        destination='snowflake',
        dataset_name="bronze"
    )

    # Fetch all the tables from the database
    source = sql_database()

    # Run the pipeline
    info = pipeline.run(source, write_disposition="replace")

    # Print load info
    print("-" * 20)
    print("Pipeline run completed.")
    print("-" * 20)
    print(info)

if __name__ == "__main__":
    load_entire_database()