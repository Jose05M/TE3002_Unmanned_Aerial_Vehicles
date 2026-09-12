# Practice 3 — Camera Access & RC Instructions

Access to the Tello's video stream and control via RC commands (continuous velocities) instead of discrete commands.

## Overview

| | |
|---|---|
| **Drone** | DJI Tello |
| **SDK** | [djitellopy](https://github.com/damiafuentes/DJITelloPy) |
| **Goal** | Stream the onboard camera and drive the drone with continuous RC velocities |

## Files

| File | Description |
|---|---|
| [`camera.py`](camera.py) | Camera access only: starts the video stream and shows it live (drone stays on the ground). |
| [`practice3.py`](practice3.py) | Flies a circular path using `send_rc_control` (constant forward speed + yaw) while recording the camera feed to `circulo.mp4`, with a final hover and a safe landing fallback on error. |

## Requirements

```bash
pip install djitellopy opencv-python
```

## How to run

```bash
python camera.py      # camera check only
python practice3.py   # circular flight + recording
```

Press `q` in the video window to exit / land early.
