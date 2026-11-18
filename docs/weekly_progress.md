# Weekly Progress

## Week 1 (10 Nov to 16 Nov)
- 10 Nov: created repo, README with status checklist, .gitignore.
- 11 Nov: wrote docs/data_design.md (ping columns, city box, stores, movement patterns).
- 12 Nov: wrote generator v1 (home to work commute, 5-minute pings, GPS noise).
- 13 Nov: wrote validate_pings.py with 12 checks and tested it on clean and damaged data.
- 14 Nov: generator v2 with --devices option (3 million pings in seconds) and a validator that reads row by row.
- 15 Nov: created Snowflake trial account, warehouse, database, schema and RAW_PINGS table with a GEOGRAPHY column; verified with a test point and a store distance check.
- 16 Nov: loaded 2,984,430 pings into Snowflake with a GEOGRAPHY column built during the load; verified counts and morning and evening spikes in Snowflake.
- 17 Nov: installed Java 17, created a Python 3.14 environment, and installed PySpark 4.1.4, Sedona 1.9.1 and pandas.
- 18 Nov: filled in the measured Store A to Store B distance in the Snowflake notes and saved the package list in requirements.txt.