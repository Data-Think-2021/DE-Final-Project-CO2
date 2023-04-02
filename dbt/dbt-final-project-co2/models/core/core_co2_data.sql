{{ config(materialized='view') }}

with source as (

    SELECT * from {{ source('core', 'stg_co2_data') }};
)
SELECT country, co2 from source
Where country NOT IN ('Asia', 'Asia (excl. China and India)', 'Europe', 
'Europe (excl. EU-27)', 'Europe (excl. EU-28)', 'European Union (27)','European Union (28)', 
'High-income countries', 'Lower-middle-income countries', 'North America', 'North America (excl. USA)', 
'European Union (27) (GCP)', 'South America', 'World', 'Upper-middle-income countries', 'others',
'OECD (GCP)') and year=2021; 



