from djitellopy import Tello
import cv2 as cv2
import time

# Initialize drone
tello = Tello()
tello.connect()

print(f"Battery: {tello.get_battery()}%")

# Initialize stream
tello.streamoff()
time.sleep(2)
tello.streamon()
time.sleep(3)

# Get access to frames
frame_read = tello.get_frame_read()

# Display 300 frames
for i in range(1000):
    frame = frame_read.frame

    if frame is None:
        print("No frame")
        continue
    else:
        print("Frame received")

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow("Tello", frame)

    # Quit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close everything
cv2.destroyAllWindows()
tello.streamoff()
