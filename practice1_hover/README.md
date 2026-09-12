# Practice 1 — Connection & Hover

First hands-on contact with the DJI Tello: verify the connection to the drone and run a basic flight (takeoff, hover, land).

## Overview

| | |
|---|---|
| **Drone** | DJI Tello |
| **SDK** | [djitellopy](https://github.com/damiafuentes/DJITelloPy) |
| **Goal** | Confirm Wi-Fi connectivity and perform a minimal safe flight |

## Files

| File | Description |
|---|---|
| [`check_connection.py`](check_connection.py) | Connects to the Tello and prints battery level and SDK version. Acts as a connectivity smoke test before flying. |
| [`practice1.py`](practice1.py) | Takes off, hovers for 5 seconds, and lands. |

## Requirements

```bash
pip install djitellopy
```

## How to run

1. Connect your computer to the Tello's Wi-Fi network.
2. Run the connection check:
   ```bash
   python check_connection.py
   ```
3. Run the test flight (clear at least 2x2 m of open space around the drone):
   ```bash
   python practice1.py
   ```

## Notes

- Make sure the drone has enough battery (`>10%`) before taking off.
- Keep a clear line of sight and enough room for an unexpected drift during hover.
