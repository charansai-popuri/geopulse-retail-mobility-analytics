# Weekly Progress

## Week 1 (10 Nov to 16 Nov)
- 10 Nov: created repo, README with status checklist, .gitignore.
- 11 Nov: wrote docs/data_design.md (ping columns, city box, stores, movement patterns).
- 12 Nov: wrote generator v1 (home to work commute, 5-minute pings, GPS noise).
- 13 Nov: wrote validate_pings.py with 12 checks and tested it on clean and damaged data.
- 14 Nov: generator v2 with --devices option (3 million pings in seconds) and a validator that reads row by row.
- 15 Nov: created Snowflake trial account, warehouse, database, schema and RAW_PINGS table with a GEOGRAPHY column; verified with a test point and a store distance check.
- 16 Nov: loaded 2,984,430 pings into Snowflake with a GEOGRAPHY column built during the load; verified counts and morning and evening spikes in Snowflake.

## Week 2 (17 Nov to 23 Nov)
- 17 Nov: installed Java 17, created a Python 3.14 environment, and installed PySpark 4.1.4, Sedona 1.9.1 and pandas.
- 18 Nov: fixed the Windows Spark startup error by placing the Sedona jar in PySpark's jars folder; the first Sedona test (a point for Store A) ran successfully. Wrote docs/spark_setup.md.
- 19 Nov: drew 500 m circles around the three stores with Sedona and joined them to the pings (small file). Store A: 428 pings from 64 devices, Store B: 501 from 62, Store C: 462 from 75, matching a plain-Python check within 2 pings. Fixed two Windows errors: Spark could not find Python (set PYSPARK_PYTHON) and ST_Buffer needed the GeoTools jar.
- 20 Nov: ran the 500 m catchment join on all 2,984,430 pings in 336 seconds with 4 GB of driver memory and no memory errors. Store A: 22,605 pings from 3,829 devices, Store B: 21,425 from 3,506, Store C: 21,153 from 3,421. Counts are within 0.25% of plain-Python checks on a sphere and on the WGS 84 ellipsoid.
- 21 Nov: counted unique visitors per store per hour on all 2,984,430 pings in 161 seconds. Store A had 1,867 devices at 9:00 and 1,868 at 18:00 against about 355 at night (3:00: 359); Stores B and C show the same morning and evening spikes. Saved the 72-row table to data/processed/hourly_visitors.csv for dbt.
- 23 Nov: created a separate Python 3.14 environment for dbt (.venv-dbt) and installed dbt Core 1.12.7 with the Snowflake adapter 1.12.5; added private-key file types to .gitignore. Next: key-pair login to Snowflake and the first dbt model.
- 24 Nov: connected dbt to Snowflake with key-pair login (dbt needs the Snowflake LOGIN_NAME as the user, not the user NAME). Loaded the 72-row hourly visitors table as a dbt seed, built two models (hourly_footfall, peak_vs_night) and ran 4 tests, all passing. Rush hours show about 1,700 unique visitors per hour at Store A against about 355 at night, about 5 times higher.

## Week 3 (24 Nov to 30 Nov)
- 25 Nov: created STORES and STORE_VISITS tables in Snowflake (devices within 500 m of each store, using ST_DWITHIN). Counts: A <your A>, B <your B>, C <your C>.