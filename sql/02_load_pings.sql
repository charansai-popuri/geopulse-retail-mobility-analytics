-- GeoPulse: load the generated pings into Snowflake.
-- Run each statement one at a time in a Snowflake workspace (Ctrl+Enter).

-- 1. A stage is a waiting area for files inside Snowflake.
CREATE STAGE IF NOT EXISTS GEOPULSE_DB.RAW.PINGS_STAGE;

-- 2. Upload data/raw/pings_large.csv by hand:
--    Ingestion > Add Data > Load files into a Stage > GEOPULSE_DB.RAW.PINGS_STAGE
--    (Snowsight allows up to 250 MB per file.)
LIST @GEOPULSE_DB.RAW.PINGS_STAGE;

-- 3. Load into the table. $1..$4 are the CSV columns DeviceID, Lat, Long, Timestamp.
--    ST_MAKEPOINT takes longitude first, then latitude.
COPY INTO GEOPULSE_DB.RAW.RAW_PINGS (DEVICE_ID, LATITUDE, LONGITUDE, PING_TS, LOCATION)
FROM (
  SELECT t.$1,
         t.$2::FLOAT,
         t.$3::FLOAT,
         TO_TIMESTAMP_NTZ(t.$4),
         ST_MAKEPOINT(t.$3::FLOAT, t.$2::FLOAT)
  FROM @GEOPULSE_DB.RAW.PINGS_STAGE t
)
FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1);

-- 4. Checks. Expected: 2984430 pings, 50000 devices, 0 missing locations.
SELECT COUNT(*) AS TOTAL_PINGS, COUNT(DISTINCT DEVICE_ID) AS DEVICES
FROM GEOPULSE_DB.RAW.RAW_PINGS;

SELECT COUNT(*) AS MISSING_LOCATION
FROM GEOPULSE_DB.RAW.RAW_PINGS WHERE LOCATION IS NULL;

-- Pings per hour: morning and evening rush hours should be the highest.
SELECT HOUR(PING_TS) AS HR, COUNT(*) AS PINGS
FROM GEOPULSE_DB.RAW.RAW_PINGS GROUP BY HR ORDER BY HR;