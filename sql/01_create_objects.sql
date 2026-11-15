-- GeoPulse: create the Snowflake objects.
-- Run each statement one at a time in a Snowflake workspace (Ctrl+Enter).

-- The warehouse is the compute engine. XSMALL is the cheapest size and it
-- switches itself off after 60 idle seconds.
CREATE WAREHOUSE IF NOT EXISTS GEOPULSE_WH
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE;

-- A database holds schemas, and a schema holds tables.
CREATE DATABASE IF NOT EXISTS GEOPULSE_DB;
CREATE SCHEMA IF NOT EXISTS GEOPULSE_DB.RAW;

-- Raw pings. LOCATION is a GEOGRAPHY column built with
-- ST_MAKEPOINT(longitude, latitude), longitude first.
-- The full name is used because USE statements did not carry over in Snowsight.
CREATE TABLE IF NOT EXISTS GEOPULSE_DB.RAW.RAW_PINGS (
  DEVICE_ID  VARCHAR(10)   NOT NULL,
  LATITUDE   FLOAT         NOT NULL,
  LONGITUDE  FLOAT         NOT NULL,
  PING_TS    TIMESTAMP_NTZ NOT NULL,
  LOCATION   GEOGRAPHY
);