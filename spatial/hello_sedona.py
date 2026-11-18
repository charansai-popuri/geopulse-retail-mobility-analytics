from sedona.spark import SedonaContext

# Start a local Spark session. The Sedona jar is already in PySpark's jars folder.
config = (
    SedonaContext.builder()
    .appName("geopulse-hello")
    .master("local[*]")
    .getOrCreate()
)
sedona = SedonaContext.create(config)

# Ask Sedona to build one point: Store A (longitude first, then latitude).
df = sedona.sql("SELECT ST_Point(77.5946, 12.9716) AS store_a")
df.show(truncate=False)