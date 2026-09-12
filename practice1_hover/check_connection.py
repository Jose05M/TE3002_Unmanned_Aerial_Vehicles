from djitellopy import Tello

tello = Tello()

# Connect to the drone
tello.connect()

# Get battery level (acts as a connection test)
battery = tello.get_battery()
print("Battery:", battery)

# You can also print SDK info
print("SDK:", tello.query_sdk_version())