# Practice 2 — Translations & Basic Trajectories

Basic Tello movements (forward/back, lateral, altitude, rotation) combined into simple geometric trajectories.

## Overview

| | |
|---|---|
| **Drone** | DJI Tello |
| **SDK** | [djitellopy](https://github.com/damiafuentes/DJITelloPy) |
| **Goal** | Chain basic motion commands into closed trajectories |

## Files

| File | Description |
|---|---|
| [`practice2.py`](practice2.py) | Interactive menu that runs one of four trajectories. |

### Trajectory options

1. **Square (rotation)** — advance + turn 90° x4
2. **Square (lateral)** — forward, left, back, right
3. **Triangle** — turn 120° x3
4. **Star** — advance + turn 144° x5

Battery is checked before takeoff; the script aborts if it's below 10%.

## Requirements

```bash
pip install djitellopy
```

## How to run

```bash
python practice2.py
```

1. Connect to the Tello's Wi-Fi network.
2. Choose a trajectory from the menu.
3. Clear at least 2x2 m of open space around the drone.

## Notes

- The drone climbs 50 cm before running the trajectory and descends 50 cm before landing.
