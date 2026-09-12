![Course](https://img.shields.io/badge/TE3002B-Implementaci%C3%B3n%20de%20Rob%C3%B3tica%20Inteligente-004a99)
![Module](https://img.shields.io/badge/M%C3%B3dulo-UAVs-f4a300)

# DJI Tello UAV Practices

Practical exercises and final project for the UAV module, built around a real **DJI Tello** quadrotor controlled in Python with djitellopy and OpenCV for the computer-vision parts.

## Structure

| Folder | Topic |
|---|---|
| [`practice1_hover/`](practice1_hover/README.md) | Connection check + basic takeoff/hover/land flight |
| [`practice2_translations/`](practice2_translations/README.md) | Basic motion commands chained into geometric trajectories |
| [`practice3_camera_rc/`](practice3_camera_rc/README.md) | Camera video streaming + continuous RC control |
| [`practice4_tracking/`](practice4_tracking/README.md) | Visual tracking of a colored object with PD control |
| [`final_project/`](final_project/README.md) | Autonomous patrol + visual target tracking (final project) |

Each folder has its own `README.md` with details on what the code does, requirements, and how to run it.

## Final project

**Autonomous Patrol and Visual Target Tracking using a DJI Tello UAV** — an autonomous system where the drone patrols a circular path, detects a colored target through HSV-based computer vision (OpenCV), and switches to visual servoing to track it: adjusting yaw, altitude, and distance in real time, and recovering the search pattern if the target is lost.

## Requirements

All practices need:

```bash
pip install djitellopy opencv-python numpy
```

## License

See [LICENSE](LICENSE) (Apache License 2.0).

---

Tecnológico de Monterrey, Campus Monterrey · Professor: Dr. Herman Castañeda Cuevas · Author: José Eduardo Sánchez Martínez (A01738476)
