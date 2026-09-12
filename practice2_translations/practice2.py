from djitellopy import Tello
import time

def square_rotation(tello):
    tello.move_forward(100)
    tello.rotate_clockwise(90)

    tello.move_forward(100)
    tello.rotate_clockwise(90)

    tello.move_forward(100)
    tello.rotate_clockwise(90)

    tello.move_forward(100)
    tello.rotate_clockwise(90)

def square_lateral(tello):
    tello.move_forward(100)
    tello.move_left(100)
    tello.move_back(100)
    tello.move_right(100)

def triangle(tello):
    tello.rotate_clockwise(120)
    tello.move_forward(100)

    tello.rotate_clockwise(120)
    tello.move_forward(100)

    tello.rotate_clockwise(120)
    tello.move_forward(100)

def star(tello):
        for _ in range(5):
            tello.move_forward(100)
            tello.rotate_clockwise(144)

def menu():
    print("\n--- TRAJECTORY MENU ---")
    print("1. Square (rotation)")
    print("2. Square (lateral)")
    print("3. Triangle")
    print("4. Star")
    option = input("Choose an option: ")
    return option

if __name__ == '__main__':
    tello = Tello()

    # Connect to the drone
    tello.connect()

    # Show battery level
    battery = tello.get_battery()
    print(f"Battery: {battery}%")

    if battery < 10:
        print("Low battery, not taking off")
        tello.end()
        exit()

    option = menu()

    # Takeoff
    tello.takeoff()
    time.sleep(2)

    print("Going up")
    tello.move_up(50)

    if option == "1":
        print("Running square (rotation)")
        square_rotation(tello)

    elif option == "2":
        print("Running square (lateral)")
        square_lateral(tello)

    elif option == "3":
        print("Running triangle")
        triangle(tello)

    elif option == "4":
        print("Running star")
        star(tello)

    else:
        print("Invalid option")

    print("Going down")
    tello.move_down(50)

    tello.land()

    tello.end()
    print("Drone connection closed")
