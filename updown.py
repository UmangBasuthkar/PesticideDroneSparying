from dronekit import connect, VehicleMode
import time

# Connect to the vehicle
vehicle = connect('/dev/ttyUSB0', wait_ready=True)  # Replace '/dev/ttyUSB0' with the address of your autopilot

# Arm and take off to a specified altitude (in meters)
def arm_and_takeoff(aTargetAltitude):
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialize...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)

    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

# Arm and take off to 10 meters
arm_and_takeoff(10)

# Wait for a few seconds at the target altitude
time.sleep(5)

# Land
print("Landing...")
vehicle.mode = VehicleMode("LAND")

# Close the connection
time.sleep(2)
vehicle.close()
