#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint


@task(log_prints=True, retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url)
    
    print(f"rows: {len(df)}")
    return df

@task(log_prints=True, retries=3)
def write_local(df: pd.DataFrame) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"data/owid-co2-data.csv.parquet")
    path.parent.mkdir(parents=True, exist_ok=True)  
    df.to_parquet(path, compression="gzip")

    return path

@task(log_prints=True, retries=3)
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcp_bucket_block = GcsBucket.load("de-final-project")
    gcp_bucket_block.upload_from_path(
        from_path=path,
        to_path=path
    )
    return

@flow()
def etl_web_to_gcs() -> None:
    """The main ETL function
    """
    dataset_url = f"https://nyc3.digitaloceanspaces.com/owid-public/data/co2/owid-co2-data.csv"

    df = fetch(dataset_url)
    path = write_local(df)
    write_gcs(path)


if __name__ == "__main__":
    etl_web_to_gcs()