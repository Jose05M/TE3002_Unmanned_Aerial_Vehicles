# Practice 4 — Visual Tracking

Visual tracking of a green object using PD control on yaw and altitude, based on the Tello's camera feed.

## Overview

| | |
|---|---|
| **Drone** | DJI Tello |
| **SDK** | [djitellopy](https://github.com/damiafuentes/DJITelloPy) |
| **Goal** | Keep a colored object centered in frame using closed-loop PD control |

## Files

| File | Description |
|---|---|
| [`practice4.py`](practice4.py) | Detects green via an HSV threshold, computes the centroid of the largest contour, and adjusts yaw (left/right) and altitude (up/down) with a PD controller to keep the object centered. Records the result to `tracking.mp4`. |

## Requirements

```bash
pip install djitellopy opencv-python numpy
```

## How to run

```bash
python practice4.py
```

You'll need a green object/surface for the drone to detect and follow. Press `q` to land and exit.
