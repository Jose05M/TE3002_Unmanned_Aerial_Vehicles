from djitellopy import Tello
import cv2
import numpy as np
import time


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

out = cv2.VideoWriter('tracking.mp4',cv2.VideoWriter_fourcc(*'mp4v'),15,(w, h))

# PD parameters
Kp_yaw = 0.4
Kd_yaw = 0.2
Kp_z = 0.3
Kd_z = 0.1
prev_error_yaw = 0
prev_error_z = 0

# Modes
mode = "patrol"
tracking_start = None

# HSV range (green)
lower = np.array([50, 100, 100])
upper = np.array([70, 255, 255])

tello.takeoff()
time.sleep(2)
print("Tracking started")

try:
    while True:
        frame = frame_read.frame
        if frame is None:
            continue

        frame = cv2.resize(frame, (480, 360))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)

        # Find contours
        contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        if mode == "patrol":

            # Smooth circular patrol
            tello.send_rc_control(
                0,      # left/right
                20,     # forward
                0,      # up/down
                20      # yaw
            )

        if contours:

            # Largest contour
            largest = max(contours, key=cv2.contourArea)

            area = cv2.contourArea(largest)
            #print(f"Area: {area}")

            if area > 500:
                if mode == "patrol":
                    print("TARGET DETECTED")
                    mode = "tracking"
                    tracking_start = time.time()

                x, y, w, h = cv2.boundingRect(largest)

                # Object center
                cx = x + w // 2
                cy = y + h // 2

                # Yaw control
                error_yaw = cx - 240
                derivative_yaw = error_yaw - prev_error_yaw

                yaw_speed = int(Kp_yaw * error_yaw + Kd_yaw * derivative_yaw)
                yaw_speed = int(np.clip(yaw_speed, -70, 70))

                # Z control
                error_z = 180 - cy
                derivative_z = error_z - prev_error_z

                ud = int(Kp_z * error_z + Kd_z * derivative_z)
                ud = int(np.clip(ud, -20, 20))

                # Forward control
                desired_area = 20500
                error_forward = desired_area - area

                # Hover zone
                hover_threshold = 2500

                # If target is at correct distance
                if abs(error_forward) < hover_threshold:
                    fb = 0
                # Otherwise follow target
                else:
                    fb = int(0.002 * error_forward)

                # Limit speed
                fb = int(np.clip(fb, -12, 12))

                # Send command
                if mode == "tracking":
                    tello.send_rc_control(
                        0,          # left/right
                        fb,         # forward/back
                        ud,         # up/down
                        yaw_speed   # yaw
                    )

                # Update previous errors
                prev_error_yaw = error_yaw
                prev_error_z = error_z

                # Draw
                cv2.rectangle(frame,(x, y),(x+w, y+h),(0,255,0),2)
                cv2.circle(frame,(cx, cy),5,(255,0,0),-1)
                cv2.putText(frame,"GREEN DETECTED",(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
                cv2.putText(frame,f"Yaw: {yaw_speed}",(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
                cv2.putText(frame,f"Z: {ud}",(10,90),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
                cv2.putText(frame,f"FB: {fb}",(10,120),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)

        else:
            # If tracking and target lost
            if mode == "tracking":

                # Rotate searching target again
                tello.send_rc_control(0, 0, 0, 25)
                cv2.putText(frame,"TARGET LOST - SEARCHING",(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

            else:
                cv2.putText(frame,"PATROLLING",(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255),2)

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)
        cv2.imshow("Tello Tracking", frame)

        key = cv2.waitKey(1)

        # Quit program
        if key & 0xFF == ord('q'):
            break

        # Land command
        if key & 0xFF == ord('l'):
            print("Landing command received")
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