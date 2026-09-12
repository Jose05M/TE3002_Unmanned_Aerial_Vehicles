from djitellopy import Tello
import time

if __name__ == '__main__':
    tello = Tello()

    # Connect to the drone
    tello.connect()

    # Takeoff
    tello.takeoff()

    # Hover
    print("Remaining in hover")
    time.sleep(5)

    # Land
    tello.land()

    tello.end()
    print("Drone connection closed")