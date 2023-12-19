from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from dronekit import *
hold = False
pitch = False
def buttonhold(x):
    global hold
    hold = True
def buttonpitch(y):
    global pitch
    pitch = True
def detect_object():
    # Return True if an object is detected, False otherwise
    return False
def object_movement():
    #Return true if object is moving towards
    return False
    
def arm_and_takeoff(vehicle,altitude):
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)
    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)
    print("Taking off!")
    vehicle.simple_takeoff(altitude)
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)
def pos_hold(vehicle):
    global pitch
    print("Drone Holded")
    vehicle.mode = VehicleMode("GUIDED")
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,
        0, 0,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111,
        0, 0, 0,
        0, 0, 0, # x, y, z velocity in m/s
        0, 0, 0,
        0, 0)
    k = 1
    while k <= 10:  
        vehicle.send_mavlink(msg)
        k += 1
        if(object_movement() or pitch):
            pitch = False
            pitch_back(vehicle)
            break
        time.sleep(1)
def pitch_back(vehicle):
    global pitch
    print("Pitching back")
    vehicle.mode = VehicleMode("GUIDED")
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,
        0, 0,
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED,
        0b0000111111000111,
        0, 0, 0,
        -1, 0, 0, # x, y, z velocity in m/s
        0, 0, 0,
        0, 0)
    vehicle.send_mavlink(msg)
    l = 1
    while l<=10:
        if(object_movement() or pitch):
            vehicle.send_mavlink(msg)
            pitch = False
        l += 1
        time.sleep(1)
def fly(data,altitude,groundspeed,airspeed):
    #connection_string = 'COM4'
    connection_string = "udp:127.0.0.1:14550"
    print('Connecting to vehicle on: %s' % connection_string)
    #vehicle = connect(connection_string, wait_ready=True,timeout=60,baud=57600)
    vehicle = connect(connection_string, wait_ready=True)
    flag = 0
    try:
        arm_and_takeoff(vehicle,altitude)
        print("Set default/target airspeed to {}".format(airspeed))
        vehicle.airspeed = airspeed
        global hold
        for i in range(1,len(data)):
            print("Going to point ", i-1)
            point = LocationGlobalRelative(float(data[i]['lat']),float(data[i]['lng']),altitude)
            vehicle.simple_goto(point,groundspeed=groundspeed)
            j = 1
            while j<=30:
                if(vehicle.location.global_frame.lat == data[i]['lat'] and vehicle.location.global_frame.lng == data[i]['lng']):
                    time.sleep(5)
                    break
                if detect_object() or hold:
                    flag = 1
                    hold = False
                    print("Object detected")
                    pos_hold(vehicle)
                    print("DONE")
                    break
                j += 1
                time.sleep(1)
            if flag == 1:
                break
            print("Success")
    except KeyboardInterrupt:
        print("User interrupted the program")
    finally:
        print("Going back home")
        vehicle.mode = VehicleMode("RTL")
        print("Disarming motors")
        vehicle.armed = False
        vehicle.close()