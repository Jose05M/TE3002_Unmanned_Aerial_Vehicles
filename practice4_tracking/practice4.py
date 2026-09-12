from djitellopy import Tello
import cv2
import numpy as np
import time


# Init
tello = Tello()
tello.connect()

print(f"Battery: {tello.get_battery()}%")

tello.streamoff()
time.sleep(1)

tello.streamon()
time.sleep(2)

frame_read = tello.get_frame_read()
# Wait for a valid frame
while frame_read.frame is None:
    time.sleep(0.1)

frame0 = frame_read.frame
frame0 = cv2.resize(frame0, (480, 360))

h, w, _ = frame0.shape


# Video writer
out = cv2.VideoWriter(
    'tracking.mp4',
    cv2.VideoWriter_fourcc(*'mp4v'),
    15,
    (w, h)
)

# PD parameters
Kp_yaw = 0.4
Kd_yaw = 0.2
Kp_z = 0.3
Kd_z = 0.1
prev_error_yaw = 0
prev_error_z = 0

# HSV range (green)
lower = np.array([50, 100, 100])
upper = np.array([70, 255, 255])

# Takeoff
tello.takeoff()
time.sleep(2)

print("Tracking started")

try:
    while True:
        frame = frame_read.frame
        if frame is None:
            continue

        # Resize
        frame = cv2.resize(frame, (480, 360))

        # BGR -> HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Green mask
        mask = cv2.inRange(hsv, lower, upper)

        # Find contours
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if contours:

            # Largest contour
            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)

            # Avoid noise
            if area > 1000:

                x, y, w, h = cv2.boundingRect(largest)

                # Object center
                cx = x + w // 2
                cy = y + h // 2

                # Yaw control
                error_yaw = cx - 240
                derivative_yaw = error_yaw - prev_error_yaw

                yaw_speed = int(
                    Kp_yaw * error_yaw +
                    Kd_yaw * derivative_yaw
                )

                yaw_speed = int(np.clip(yaw_speed, -70, 70))

                # Z control
                error_z = 180 - cy
                derivative_z = error_z - prev_error_z

                ud = int(
                    Kp_z * error_z +
                    Kd_z * derivative_z
                )

                ud = int(np.clip(ud, -15, 15))

                # Send command
                tello.send_rc_control(
                    0,      # left/right
                    0,      # forward/back
                    ud,     # up/down
                    yaw_speed
                )

                # Update previous errors
                prev_error_yaw = error_yaw
                prev_error_z = error_z

                # Draw
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x+w, y+h),
                    (0,255,0),
                    2
                )

                cv2.circle(
                    frame,
                    (cx, cy),
                    5,
                    (255,0,0),
                    -1
                )

                cv2.putText(
                    frame,
                    "GREEN DETECTED",
                    (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,0,255),
                    2
                )

                cv2.putText(
                    frame,
                    f"Yaw: {yaw_speed}",
                    (10,60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255,255,255),
                    2
                )

                cv2.putText(
                    frame,
                    f"Z: {ud}",
                    (10,90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255,255,255),
                    2
                )

        else:

            # No object detected
            tello.send_rc_control(0,0,0,0)

            cv2.putText(
                frame,
                "NO GREEN DETECTED",
                (10,30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,0,255),
                2
            )

        # Display        
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)
        cv2.imshow("Tello Tracking", frame)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Interrupted")

finally:

    print("Landing...")
    tello.send_rc_control(0,0,0,0)
    time.sleep(1)
    tello.land()

    tello.streamoff()
    out.release()

    cv2.destroyAllWindows()
    print("✅ Finished")