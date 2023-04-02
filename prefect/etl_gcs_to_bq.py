#!/usr/bin/env python
# coding: utf-8
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
from prefect.tasks import task_input_hash
from datetime import timedelta


@task(log_prints=True, retries=3) # , cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1)
def extract_from_gcs() -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/owid-co2-data.csv.parquet"
    gcp_bucket_block = GcsBucket.load("de-final-project")
    gcp_bucket_block.get_directory(
        from_path=gcs_path
    )
    df = pd.read_parquet(gcs_path)
    return df

@task(log_prints=True, retries=3)
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BigQuery"""
    gcp_credentials_block = GcpCredentials.load("de-final-project")
    credential = gcp_credentials_block.get_credentials_from_service_account()

    df.to_gbq(
        destination_table="co2_data.dl_co2_data",
        project_id="de-finalproject",
        credentials=credential,
        if_exists="append",
    )


@flow()
def etl_gcs_to_bq() -> None:
    """The main ETL function to load data into BigQuery"""
    df = extract_from_gcs()
    write_bq(df)


if __name__ == "__main__":
    etl_gcs_to_bq()