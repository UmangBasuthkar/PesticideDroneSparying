from dronekit import connect, VehicleMode
import time
from lidar import lidar_sensor
lidar_sensor = LidarSensor("")
vehicle = connect('udp:127.0.0.1:14550', wait_ready=True)
def get_lidar_distance():
    distance = lidar_sensor.get_distance()
    return distance
def move_away():
    print("Obstacle detected! Moving away...")
    vehicle.simple_goto(vehicle.location.global_relative_frame + (0.001, 0, 0))
try:
    while True:
        lidar_distance = get_lidar_distance()
        obstacle_threshold = 5.0 
        if lidar_distance < obstacle_threshold:
            move_away()
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    vehicle.close()
