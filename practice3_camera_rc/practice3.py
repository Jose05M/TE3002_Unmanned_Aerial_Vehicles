from djitellopy import Tello
import cv2
import time

# --- Init ---
tello = Tello()
tello.connect()
print(f"Battery: {tello.get_battery()}%")

# --- Stream ---
tello.streamoff()
time.sleep(2)
tello.streamon()
time.sleep(3)

frame_read = tello.get_frame_read()

# Wait for a valid frame
for _ in range(50):
    if frame_read.frame is not None:
        break
    time.sleep(0.1)

frame = frame_read.frame
h, w, _ = frame.shape

# --- VideoWriter ---
out = cv2.VideoWriter('circulo.mp4',
                      cv2.VideoWriter_fourcc(*'mp4v'),
                      30,
                      (w, h))

cv2.namedWindow("Tello", cv2.WINDOW_NORMAL)

# --- Takeoff ---
tello.takeoff()
time.sleep(2)

print("Starting circle + recording")

# Parameters
forward = 30
yaw = 40
dt = 0.05
duration = 14   # seconds
loops = int(duration / dt)

try:
    # --- Circular movement + video ---
    for i in range(loops):
        frame = frame_read.frame
        if frame is None:
            continue

        # Display
        frame_show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow("Tello", frame_show)

        # Save (without converting)
        out.write(frame)

        # Movement (equivalent to rc(a=0,b=30,c=0,d=40))
        tello.send_rc_control(0, forward, 0, yaw)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(dt)

    # --- Stop ---
    tello.send_rc_control(0, 0, 0, 0)
    time.sleep(1)

    # --- Hover (3s) ---
    print("Hover")
    hover_loops = int(3 / dt)
    for _ in range(hover_loops):
        frame = frame_read.frame
        if frame is not None:
            frame_show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imshow("Tello", frame_show)
            out.write(frame)

        tello.send_rc_control(0, 0, 0, 0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(dt)

finally:
    # --- Safe landing ---
    print("Landing...")
    try:
        tello.land()
    except:
        tello.send_rc_control(0,0,0,0)
        time.sleep(2)
        tello.land()

    out.release()
    cv2.destroyAllWindows()
    tello.streamoff()

    print("✅ Done: circulo.mp4")
