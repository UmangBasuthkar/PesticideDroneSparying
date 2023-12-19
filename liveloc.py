from dronekit import connect, VehicleMode
import time
connection_string = 'COM4'
vehicle = connect(connection_string, wait_ready=True,timeout=60,baud=57600)
print(vehicle.location.global_frame)
try:
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    while True:
        location = vehicle.location.global_frame
        print("Latitude: %s, Longitude: %s, Altitude: %s" % (location.lat, location.lon, location.alt))
        time.sleep(1) 

except KeyboardInterrupt:
    print("User interrupted the script.")

finally:
    vehicle.close()
