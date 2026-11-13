"""GeoPulse ping validator (version 1).

Reads data/raw/pings.csv and runs simple quality checks.
Prints PASS or FAIL for each check.
"""

import csv
import os
import re
import sys
from collections import Counter
from datetime import datetime

# ----- Settings (must match generate_pings.py) -----
INPUT_FILE = os.path.join("data", "raw", "pings.csv")
EXPECTED_HEADER = ["DeviceID", "Lat", "Long", "Timestamp"]
LAT_MIN, LAT_MAX = 12.90, 13.00
LONG_MIN, LONG_MAX = 77.55, 77.65
TOLERANCE = 0.001          # allows for GPS noise (about 100 metres)
PEAK_FACTOR = 1.5          # rush hours must be 1.5x busier than night

results = []


def check(name, passed, detail=""):
    """Record and print one check result."""
    results.append(passed)
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}" + (f" - {detail}" if detail else ""))


def main():
    if not os.path.exists(INPUT_FILE):
        print(f"File not found: {INPUT_FILE}. Run generate_pings.py first.")
        sys.exit(1)

    with open(INPUT_FILE, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    check("1. Header is DeviceID,Lat,Long,Timestamp", header == EXPECTED_HEADER)
    check("2. File has at least one ping", len(rows) > 0, f"{len(rows)} rows")

    missing = sum(1 for r in rows if len(r) != 4 or any(v.strip() == "" for v in r))
    check("3. No missing values", missing == 0, f"{missing} bad rows")

    good = [r for r in rows if len(r) == 4 and all(v.strip() != "" for v in r)]

    bad_ids = sum(1 for r in good if not re.fullmatch(r"D\d{6}", r[0]))
    check("4. DeviceID format is D + 6 digits", bad_ids == 0, f"{bad_ids} bad IDs")

    out_of_box = 0
    bad_numbers = 0
    for r in good:
        try:
            lat, lon = float(r[1]), float(r[2])
        except ValueError:
            bad_numbers += 1
            continue
        if not (LAT_MIN - TOLERANCE <= lat <= LAT_MAX + TOLERANCE
                and LONG_MIN - TOLERANCE <= lon <= LONG_MAX + TOLERANCE):
            out_of_box += 1
    check("5. Lat and Long are numbers", bad_numbers == 0, f"{bad_numbers} bad rows")
    check("6. All pings inside the city box", out_of_box == 0, f"{out_of_box} outside")

    stamps = []
    bad_time = 0
    for r in good:
        try:
            stamps.append(datetime.strptime(r[3], "%Y-%m-%d %H:%M:%S"))
        except ValueError:
            bad_time += 1
    check("7. Timestamps have the right format", bad_time == 0, f"{bad_time} bad rows")

    days = {s.date() for s in stamps}
    check("8. All pings are on one day", len(days) == 1,
          f"days found: {sorted(str(d) for d in days)}")

    pairs = Counter((r[0], r[3]) for r in good)
    dupes = sum(1 for c in pairs.values() if c > 1)
    check("9. No duplicate (DeviceID, Timestamp)", dupes == 0, f"{dupes} duplicates")

    devices = {r[0] for r in good}
    check("10. Number of devices", len(devices) > 0, f"{len(devices)} devices")

    per_hour = Counter(s.hour for s in stamps)
    night = sum(per_hour[h] for h in range(0, 6)) / 6
    morning = max(per_hour[8], per_hour[9])
    evening = max(per_hour[17], per_hour[18])
    check("11. Morning rush is busier than night", morning >= PEAK_FACTOR * night,
          f"morning peak {morning} vs night average {night:.0f}")
    check("12. Evening rush is busier than night", evening >= PEAK_FACTOR * night,
          f"evening peak {evening} vs night average {night:.0f}")

    passed = sum(results)
    print(f"\n{passed} of {len(results)} checks passed.")
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()