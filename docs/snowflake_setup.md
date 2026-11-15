# Snowflake Setup

## Account
- Snowflake trial account created 15 Nov 2026 (30-day trial), AWS Asia Pacific (Thailand).
- Credentials are kept privately and never stored in this repository.

## Objects (see sql/01_create_objects.sql)
| Object | Name | Purpose |
|---|---|---|
| Warehouse | GEOPULSE_WH | XSMALL compute, auto-suspends after 60 seconds |
| Database | GEOPULSE_DB | Holds all GeoPulse data |
| Schema | RAW | Untouched source pings |
| Table | GEOPULSE_DB.RAW.RAW_PINGS | DEVICE_ID, LATITUDE, LONGITUDE, PING_TS, LOCATION (GEOGRAPHY) |

## Notes
- GEOGRAPHY uses WGS 84 (SRID 4326), and longitude comes first: ST_MAKEPOINT(longitude, latitude).
- In the Snowsight workspace the USE statements did not carry over between runs,
  so the SQL uses fully qualified names (GEOPULSE_DB.RAW.RAW_PINGS).

## Verification
- SHOW TABLES IN SCHEMA GEOPULSE_DB.RAW lists RAW_PINGS (0 rows before loading).
- A test point inserted with ST_MAKEPOINT read back as POINT(77.552332 12.963762).
- ST_DISTANCE between Store A and Store B was NUMBER metres (design target: about 600 m).

## Next
- Load data/raw/pings_large.csv into RAW_PINGS and compare the row count with 2,984,430.