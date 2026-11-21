import argparse
import os
import sys
import time

import pandas as pd
from sedona.spark import SedonaContext

# Tell Spark to use this same Python (the .venv one) for its helper workers.
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

parser = argparse.ArgumentParser()
parser.add_argument("--file", default="data/raw/pings.csv", help="CSV of pings to join")
parser.add_argument(
    "--output",
    default="data/processed/hourly_visitors.csv",
    help="where to save the hourly table",
)
args = parser.parse_args()
start = time.time()

config = (
    SedonaContext.builder()
    .appName("geopulse-hourly")
    .master("local[*]")
    .config("spark.driver.memory", "4g")
    .getOrCreate()
)
sedona = SedonaContext.create(config)

# 1. Load the pings and the stores
pings_pd = pd.read_csv(args.file)
sedona.createDataFrame(pings_pd).createOrReplaceTempView("pings_raw")

stores_pd = pd.DataFrame(
    {
        "store": ["A", "B", "C"],
        "lat": [12.9716, 12.9750, 12.9352],
        "lon": [77.5946, 77.5990, 77.6245],
    }
)
sedona.createDataFrame(stores_pd).createOrReplaceTempView("stores_raw")

# 2. 500 m circles around the stores
sedona.sql("""
    SELECT store,
           ST_Buffer(ST_Point(lon, lat), 500, true, 'quad_segs=32') AS catchment
    FROM stores_raw
""").createOrReplaceTempView("catchments")

# 3. Pings as points, with the hour of the day (0 to 23)
sedona.sql("""
    SELECT DeviceID,
           HOUR(TO_TIMESTAMP(Timestamp)) AS hour,
           ST_Point(CAST(Long AS DOUBLE), CAST(Lat AS DOUBLE)) AS point
    FROM pings_raw
""").createOrReplaceTempView("pings")

# 4. Unique devices per store per hour
result = sedona.sql("""
    SELECT c.store,
           p.hour,
           COUNT(DISTINCT p.DeviceID) AS unique_visitors
    FROM pings p
    JOIN catchments c ON ST_Contains(c.catchment, p.point)
    GROUP BY c.store, p.hour
    ORDER BY c.store, p.hour
""")

# 5. Bring the small result (72 rows) back to pandas, save it, print it
result_pd = result.toPandas()
os.makedirs(os.path.dirname(args.output), exist_ok=True)
result_pd.to_csv(args.output, index=False)

table = result_pd.pivot(index="hour", columns="store", values="unique_visitors")
print(table.fillna(0).astype(int).to_string())
print(f"Saved {len(result_pd)} rows to {args.output}")
print(f"Finished {len(pings_pd):,} pings in {time.time() - start:.1f} seconds")