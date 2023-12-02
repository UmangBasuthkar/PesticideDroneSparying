import subprocess
def command(latitude, longitude):
    command1 = "dronekit-sitl copter --home=" + latitude + "," + longitude + ",0,180"
    command2 = "python C:\\Python27\\Scripts\\mavproxy.py --master tcp:127.0.0.1:5760 --sitl 127.0.0.1:5501 --out 127.0.0.1:14550 --out 127.0.0.1:14551"
    subprocess.Popen(["start", "cmd", "/k", command1], shell=True)
    subprocess.Popen(["start", "cmd", "/k", command2], shell=True)
