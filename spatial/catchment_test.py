import pandas as pd
from sedona.spark import SedonaContext

config = (
    SedonaContext.builder()
    .appName("geopulse-catchment")
    .master("local[*]")
    .getOrCreate()
)
sedona = SedonaContext.create(config)

# 1. Load the pings with pandas and hand them to Spark
pings_pd = pd.read_csv("data/raw/pings.csv")
sedona.createDataFrame(pings_pd).createOrReplaceTempView("pings_raw")

# 2. The three stores
stores_pd = pd.DataFrame(
    {
        "store": ["A", "B", "C"],
        "lat": [12.9716, 12.9750, 12.9352],
        "lon": [77.5946, 77.5990, 77.6245],
    }
)
sedona.createDataFrame(stores_pd).createOrReplaceTempView("stores_raw")

# 3. Turn each store into a 500 m circle (a polygon)
sedona.sql("""
    SELECT store,
           ST_Buffer(ST_Point(lon, lat), 500, true, 'quad_segs=32') AS catchment
    FROM stores_raw
""").createOrReplaceTempView("catchments")

# 4. Turn each ping into a point
sedona.sql("""
    SELECT DeviceID, Timestamp,
           ST_Point(CAST(Long AS DOUBLE), CAST(Lat AS DOUBLE)) AS point
    FROM pings_raw
""").createOrReplaceTempView("pings")

# 5. Spatial join: keep each ping that falls inside a circle, then count
result = sedona.sql("""
    SELECT c.store,
           COUNT(*) AS pings,
           COUNT(DISTINCT p.DeviceID) AS devices
    FROM pings p
    JOIN catchments c ON ST_Contains(c.catchment, p.point)
    GROUP BY c.store
    ORDER BY c.store
""")
result.show()