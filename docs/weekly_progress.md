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
- 20 Nov: ran the 500 m catchment join on all 2,984,430 pings in N seconds with 4 GB of driver memory. Store A: P1 pings from D1 devices, Store B: P2 from D2, Store C: P3 from D3; counts match a plain-Python check within 0.5%.