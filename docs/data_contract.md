# Data contract, the columns of the lap table

| Column | Meaning |
|---|---|
| `season`, `round`, `circuit_id` | Which race |
| `constructor_id` | Stable team id |
| `driver_code` | Only for joins, never a feature |
| `lap_number`, `stint`, `compound`, `tyre_life` | Tyre context |
| `lap_time_s` | Lap time in seconds |
| `is_in_lap`, `is_out_lap`, `is_lap_one` | Pit and start flags |
| `track_status_flag`, `is_wet` | Safety car, VSC, red flag and wet, as flags |
| `is_valid` | The cleaning verdict |