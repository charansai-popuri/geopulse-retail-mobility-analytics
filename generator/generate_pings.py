"""GeoPulse mock GPS ping generator (version 2).

Creates anonymized mobile device pings for one day:
DeviceID, Lat, Long, Timestamp
Each device has a home and work location and follows a simple daily routine.

Version 2 adds command-line options so you can make much bigger files:
    python generator\\generate_pings.py --devices 50000
"""

import argparse
import csv
import os
import random
import time
from datetime import datetime, timedelta

# ----- Settings you can change -----
DEFAULT_SEED = 42              # same seed -> same data every run
DEFAULT_DEVICES = 1000         # how many phones to simulate
DAY = datetime(2026, 11, 9)    # the day to simulate (Monday)
LAT_MIN, LAT_MAX = 12.90, 13.00
LONG_MIN, LONG_MAX = 77.55, 77.65
DEFAULT_OUTPUT = os.path.join("data", "raw", "pings.csv")

STEP_MINUTES = 5               # check every 5 minutes
STILL_PING_EVERY = 30          # a device that is not moving pings every 30 min
JITTER = 0.0002                # about 20 metres of GPS noise (in degrees)

# Pre-build the 288 timestamp texts of the day once (faster than rebuilding them)
TIMESTAMPS = {
    minute: (DAY + timedelta(minutes=minute)).strftime("%Y-%m-%d %H:%M:%S")
    for minute in range(0, 24 * 60, STEP_MINUTES)
}


def make_device(index):
    """Create one device with a home, a work place and routine times."""
    return {
        "id": f"D{index:06d}",
        "home": (random.uniform(LAT_MIN, LAT_MAX), random.uniform(LONG_MIN, LONG_MAX)),
        "work": (random.uniform(LAT_MIN, LAT_MAX), random.uniform(LONG_MIN, LONG_MAX)),
        "leave_home": random.randint(8 * 60, 9 * 60 + 30),    # minute of day
        "leave_work": random.randint(17 * 60, 18 * 60 + 30),
        "trip_minutes": random.randint(25, 45),
        "offset": random.randint(0, STILL_PING_EVERY - 1),
    }


def position_and_moving(dev, minute):
    """Return (lat, long, is_moving) for a device at a minute of the day."""
    home, work = dev["home"], dev["work"]
    morning_end = dev["leave_home"] + dev["trip_minutes"]
    evening_end = dev["leave_work"] + dev["trip_minutes"]

    if minute < dev["leave_home"]:
        return home[0], home[1], False
    if minute < morning_end:
        f = (minute - dev["leave_home"]) / dev["trip_minutes"]
        return home[0] + f * (work[0] - home[0]), home[1] + f * (work[1] - home[1]), True
    if minute < dev["leave_work"]:
        return work[0], work[1], False
    if minute < evening_end:
        f = (minute - dev["leave_work"]) / dev["trip_minutes"]
        return work[0] + f * (home[0] - work[0]), work[1] + f * (home[1] - work[1]), True
    return home[0], home[1], False


def main():
    parser = argparse.ArgumentParser(description="Generate mock GPS pings.")
    parser.add_argument("--devices", type=int, default=DEFAULT_DEVICES,
                        help="number of phones to simulate (default 1000)")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED,
                        help="random seed (default 42)")
    parser.add_argument("--output", default=DEFAULT_OUTPUT,
                        help="CSV file to write (default data/raw/pings.csv)")
    args = parser.parse_args()

    started = time.time()
    random.seed(args.seed)
    devices = [make_device(i + 1) for i in range(args.devices)]
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    rows = 0
    with open(args.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["DeviceID", "Lat", "Long", "Timestamp"])
        for number, dev in enumerate(devices, start=1):
            batch = []                      # all pings of this one device
            for minute in range(0, 24 * 60, STEP_MINUTES):
                lat, lon, moving = position_and_moving(dev, minute)
                if moving or (minute + dev["offset"]) % STILL_PING_EVERY < STEP_MINUTES:
                    lat += random.uniform(-JITTER, JITTER)
                    lon += random.uniform(-JITTER, JITTER)
                    batch.append([dev["id"], f"{lat:.6f}", f"{lon:.6f}", TIMESTAMPS[minute]])
            writer.writerows(batch)         # write the whole batch in one go
            rows += len(batch)
            if number % 10000 == 0:
                print(f"  ... {number} of {args.devices} devices done")

    size_mb = os.path.getsize(args.output) / (1024 * 1024)
    seconds = time.time() - started
    print(f"Wrote {rows} pings for {args.devices} devices to {args.output} "
          f"({size_mb:.1f} MB, {seconds:.1f} seconds)")


if __name__ == "__main__":
    main()