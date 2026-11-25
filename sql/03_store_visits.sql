-- GeoPulse: which devices visit which store (Week 3, cannibalization).
-- Run each statement one at a time in a Snowflake workspace (Ctrl+Enter).

-- 1. Stores table. ST_MAKEPOINT takes longitude first, then latitude.
CREATE OR REPLACE TABLE GEOPULSE_DB.RAW.STORES AS
SELECT STORE, LATITUDE, LONGITUDE,
       ST_MAKEPOINT(LONGITUDE, LATITUDE) AS LOCATION
FROM VALUES
  ('A', 12.9716, 77.5946),
  ('B', 12.9750, 77.5990),
  ('C', 12.9352, 77.6245)
AS s(STORE, LATITUDE, LONGITUDE);

-- 2. One row per device and store that device visited (within 500 m).
CREATE OR REPLACE TABLE GEOPULSE_DB.RAW.STORE_VISITS AS
SELECT DISTINCT p.DEVICE_ID, s.STORE
FROM GEOPULSE_DB.RAW.RAW_PINGS p
JOIN GEOPULSE_DB.RAW.STORES s
  ON ST_DWITHIN(p.LOCATION, s.LOCATION, 500);

-- 3. Check. Expected: A about 3824, B about 3497, C about 3420.
SELECT STORE, COUNT(*) AS DEVICES
FROM GEOPULSE_DB.RAW.STORE_VISITS
GROUP BY STORE ORDER BY STORE;