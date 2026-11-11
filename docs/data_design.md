# GeoPulse Data Design

## Purpose
The generator creates mock, anonymized mobile GPS pings that imitate how
people move through a city during a day. Later steps join these pings to
store catchment areas to measure footfall and cannibalization.

## Ping table columns
| Column | Type | Meaning |
|---|---|---|
| DeviceID | text | Anonymous ID of one phone, for example D000123 |
| Lat | decimal | Latitude of the ping |
| Long | decimal | Longitude of the ping |
| Timestamp | datetime | When the ping was recorded |

## City area
A box of about 10 km by 10 km:
- Latitude from 12.90 to 13.00
- Longitude from 77.55 to 77.65

## Stores (500 m catchment around each)
| Store | Lat | Long | Role |
|---|---|---|---|
| Store A | 12.9716 | 77.5946 | Existing store |
| Store B | 12.9750 | 77.5990 | Proposed store, about 600 m from Store A |
| Store C | 12.9352 | 77.6245 | Far away, used for comparison |

Store A and Store B are close on purpose, so their catchment areas overlap.
This lets us test the cannibalization question.

## Movement patterns (planned)
- Morning commute: 8:00 to 10:00, devices travel from home areas to work areas
- Lunch: 12:30 to 14:00, short trips near work areas
- Evening commute: 17:00 to 19:30, devices travel back home
- Night: few pings, devices mostly stay at home

## Size plan
- Start with 10,000 devices to test the code
- Increase to millions of pings for the Spark spatial join test
- Ping interval about every 5 minutes while a device is active

## Validation checks (planned)
- No missing values in any column
- All Lat and Long inside the city box
- Timestamps in the expected date range
- Morning and evening hours show higher ping counts than night