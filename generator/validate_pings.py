"""GeoPulse ping validator (version 2).

Reads a pings CSV one row at a time (so it works on millions of rows without
using much memory) and runs quality checks. Prints PASS or FAIL for each check.

Usage:
    python generator\\validate_pings.py
    python generator\\validate_pings.py --file data\\raw\\pings_large.csv
"""

import argparse
import csv
import os
import re
import sys
from collections import Counter
from datetime import datetime

# ----- Settings (must match generate_pings.py) -----
DEFAULT_FILE = os.path.join("data", "raw", "pings.csv")
EXPECTED_HEADER = ["DeviceID", "Lat", "Long", "Timestamp"]
LAT_MIN, LAT_MAX = 12.90, 13.00
LONG_MIN, LONG_MAX = 77.55, 77.65
TOLERANCE = 0.001          # allows for GPS noise (about 100 metres)
PEAK_FACTOR = 1.5          # rush hours must be 1.5x busier than night
ID_PATTERN = re.compile(r"D\d{6}")

results = []


def check(name, passed, detail=""):
    """Record and print one check result."""
    results.append(passed)
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}" + (f" - {detail}" if detail else ""))


def main():
    parser = argparse.ArgumentParser(description="Validate a GeoPulse pings CSV.")
    parser.add_argument("--file", default=DEFAULT_FILE, help="CSV file to check")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"File not found: {args.file}. Run generate_pings.py first.")
        sys.exit(1)

    # Counters that we update while reading the file row by row
    total = 0
    missing = 0
    bad_ids = 0
    bad_numbers = 0
    out_of_box = 0
    bad_time = 0
    duplicates = 0           # same device, same time (or time going backwards)
    devices = set()
    days = set()
    per_hour = Counter()
    last_device = None
    last_stamp = None

    with open(args.file, newline="") as f:
        reader = csv.reader(f)
        header = next(reader, [])
        for row in reader:
            total += 1
            if len(row) != 4 or any(v.strip() == "" for v in row):
                missing += 1
                continue
            device, lat_text, lon_text, stamp_text = row

            if not ID_PATTERN.fullmatch(device):
                bad_ids += 1
            devices.add(device)

            try:
                lat, lon = float(lat_text), float(lon_text)
                if not (LAT_MIN - TOLERANCE <= lat <= LAT_MAX + TOLERANCE
                        and LONG_MIN - TOLERANCE <= lon <= LONG_MAX + TOLERANCE):
                    out_of_box += 1
            except ValueError:
                bad_numbers += 1

            try:
                stamp = datetime.strptime(stamp_text, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                bad_time += 1
                continue
            days.add(stamp.date())
            per_hour[stamp.hour] += 1

            # The generator writes each device's pings together, oldest first.
            # So a repeated or earlier time for the same device is a problem.
            if device == last_device and stamp <= last_stamp:
                duplicates += 1
            last_device, last_stamp = device, stamp

    check("1. Header is DeviceID,Lat,Long,Timestamp", header == EXPECTED_HEADER)
    check("2. File has at least one ping", total > 0, f"{total} rows")
    check("3. No missing values", missing == 0, f"{missing} bad rows")
    check("4. DeviceID format is D + 6 digits", bad_ids == 0, f"{bad_ids} bad IDs")
    check("5. Lat and Long are numbers", bad_numbers == 0, f"{bad_numbers} bad rows")
    check("6. All pings inside the city box", out_of_box == 0, f"{out_of_box} outside")
    check("7. Timestamps have the right format", bad_time == 0, f"{bad_time} bad rows")
    check("8. All pings are on one day", len(days) == 1,
          f"days found: {sorted(str(d) for d in days)}")
    check("9. No duplicate or out-of-order pings per device", duplicates == 0,
          f"{duplicates} problems")
    check("10. Number of devices", len(devices) > 0, f"{len(devices)} devices")

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