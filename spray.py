from __future__ import print_function
import time
from pymavlink import mavutil
from dronekit import connect, VehicleMode, LocationGlobalRelative,Command
from dronekit import *
from math import radians, sin, cos, sqrt, atan2
connection_string = 'COM4'
vehicle = connect(connection_string,wait_ready=True,baud=57600,timeout=60)
cmd =vehicle.message_factory.command_long_encode( 1, 0, mavutil.mavlink.MAV_CMD_DO_SET_SERVO, 0, 5, 2000, 0, 0, 0, 0, 0)
vehicle.send_mavlink(cmd)
time.sleep(5)
cmd =vehicle.message_factory.command_long_encode( 1, 0, mavutil.mavlink.MAV_CMD_DO_SET_SERVO, 0, 5, 900, 0, 0, 0, 0, 0)
vehicle.send_mavlink(cmd)
print("Done")