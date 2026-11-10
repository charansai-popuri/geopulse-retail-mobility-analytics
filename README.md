# GeoPulse: Hyper-Local Retail Mobility Analytics

Infotact Solutions internship, Batch-22, Data Analytics (solo project).
Period: 10 Nov 2026 to 10 Dec 2026.

## Problem
Retailers pick store locations from static census data and risk opening a
store that cannibalizes an existing one. GeoPulse uses mobile GPS pings to
measure real foot traffic around store locations.

## Pipeline
Python ping generator -> Snowflake (GEOGRAPHY) -> Apache Sedona spatial joins
-> dbt hourly footfall models -> Kepler.gl map -> Airflow daily runs

## Status
- [ ] Week 1: mock GPS ping generator, Snowflake setup and data load
- [ ] Week 2: Sedona 500 m catchment joins, dbt hourly unique visitors
- [ ] Mid review: spatial audit and data integrity check
- [ ] Week 3: cannibalization SQL, Kepler.gl map in React
- [ ] Week 4: Airflow automation, 3D H3 hexagons, 24-hour animation
- [ ] Final: report, PPT, demo

## How to run
Coming soon (added as each module is built).