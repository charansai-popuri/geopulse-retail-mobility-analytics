"""Make a CSV that Kepler.gl can show: one row per store per hour, with coordinates."""
import csv
import os

STORES = {"A": (12.9716, 77.5946), "B": (12.9750, 77.5990), "C": (12.9352, 77.6245)}

src = os.path.join("data", "processed", "hourly_visitors.csv")
dst = os.path.join("data", "processed", "kepler_hourly_visitors.csv")

rows = []
with open(src, newline="") as f:
    for r in csv.DictReader(f):
        lat, lon = STORES[r["store"]]
        rows.append({
            "store": r["store"],
            "latitude": lat,
            "longitude": lon,
            "hour": int(r["hour"]),
            "time": "2026-11-01 %02d:00:00" % int(r["hour"]),
            "unique_visitors": int(r["unique_visitors"]),
        })

with open(dst, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

print("Wrote", len(rows), "rows to", dst)