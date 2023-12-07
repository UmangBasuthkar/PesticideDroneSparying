from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from dronekit import *
from math import radians,sin,cos,sqrt,atan2

def fly(data,altitude,groundspeed,airspeed,preex):
    connection_string = 'udp:127.0.0.1:14550'
    print('Connecting to vehicle on: %s' % connection_string)
    vehicle = connect(connection_string, wait_ready=True)
    def detect_object():
        # Return True if an object is detected, False otherwise
        return False
    
    def object_movement():
        #Return true if object is moving towards
        return False
    def getdistance(lat1, lon1, lat2, lon2):
        R = 6371000.0
        lat1_rad = radians(lat1)
        lon1_rad = radians(lon1)
        lat2_rad = radians(lat2)
        lon2_rad = radians(lon2)
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Haversine formula to calculate distance
        a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Distance in meters
        distance = R * c

        timer=round(distance//6)
        return int(timer)
    
    def arm_and_takeoff():
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

    def fetchcontainerval(initval): 
        if(initval<=0): 
            print("Tank has ran out of pesticide") 
        elif(0<initval<0.5): 
            print("Tank is running out of pesticide") 
            print("Current Tank volume: ",initval) 
        else: 
            print("Current Tank volume: ",initval) 
        preex=initval-0.060
        return preex

    def pos_hold():
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
            if(object_movement()):
                pitch_back()
                break
            time.sleep(1)

    def pitch_back():
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
            if(object_movement()):
                vehicle.send_mavlink(msg)
            l += 1
            time.sleep(1)
    flag = 0
    try:
        arm_and_takeoff()
        print("Set default/target airspeed to {}".format(airspeed))
        vehicle.airspeed = airspeed
        for i in range(1,len(data)):
            print("Going to point ", i)
            point1 = LocationGlobalRelative(float(data[i]['lat']),float(data[i]['lng']),altitude)
            t=getdistance(float(data[i-1]['lat']),float(data[i-1]['lng']),float(data[i]['lat']),float(data[i]['lng']))
            vehicle.simple_goto(point1,groundspeed=groundspeed)
            if(i>1): 
                for k in range(0,t):
                    vall=preex
                    preex=fetchcontainerval(vall) 
                    if detect_object():
                        flag = 1
                        print("Object detected")
                        pos_hold()
                        print("DONE")
                        break
                    time.sleep(1)
            else:
                time.sleep(10)
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
    print("Returning to Launch")
    vehicle.mode = VehicleMode("RTL")
    print("Close vehicle object")
    vehicle.close()