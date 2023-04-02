{{ config(materialized='view') }}

with source as (

    select * from {{ source('staging', 'dl_co2_data') }}
)
select
    GENERATE_UUID() AS id,
    country,
    year,
    date(year, 12, 30)  as year_date,
    iso_code, 
    population,
    gdp,
    cement_co2,
    cement_co2_per_capita,
    co2,
    co2_growth_abs,
    co2_including_luc,
    co2_including_luc_growth_abs,
    co2_per_capita,
    co2_per_gdp,
    co2_per_unit_energy,
    coal_co2,
    coal_co2_per_capita,
    consumption_co2,
    consumption_co2_per_capita,
    consumption_co2_per_gdp,
    cumulative_cement_co2,
    cumulative_co2,
    cumulative_co2_including_luc,
    cumulative_coal_co2,
    cumulative_flaring_co2,
    cumulative_gas_co2,
    cumulative_luc_co2,
    cumulative_oil_co2,
    cumulative_other_co2,
    energy_per_capita,
    energy_per_gdp,
    flaring_co2,
    flaring_co2_per_capita,
    gas_co2,
    land_use_change_co2,
    methane,
    methane_per_capita,
    nitrous_oxide,
    oil_co2,
    other_industry_co2,
    primary_energy_consumption,
    total_ghg,
    total_ghg_excluding_lucf
    trade_co2,
    trade_co2_share
from source


