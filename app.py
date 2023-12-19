from flask import Flask, render_template, request,jsonify
import time
from dronekit import connect, VehicleMode
app = Flask(__name__)
@app.route('/')
def index():
    return render_template("main.html")

@app.route('/startMission')
def startmission():
    return render_template("Test.html")
@app.route("/", methods=["POST"])
def process_data():
    if request.method == 'POST':
        from RunCommand import command
        data = request.get_json()
        command(str(data[0]['lat']), str(data[0]['lng']))
        time.sleep(8)
        connection_string = "udp:127.0.0.1:14550"
        vehicle = connect(connection_string,wait_ready=True)
        print("connected")
        vehicle.close()
        from Test import fly
        fly(data,5, float(2.0), float(2.0))
        return str(data)
@app.route("/get_live_location")
def get_live_location():
    #connection_string = 'COM4'
    
    #vehicle = connect(connection_string, wait_ready=True,timeout=60,baud=57600)
    
    #location = vehicle.location.global_frame
    #live_location = {'lat': location.lat, 'lng': location.lon}
    #vehicle.close()
    live_location = {'lat':17.397228,'lng':78.490215}
    return jsonify(live_location)
'''
@app.route("/data",methods=["POST"])
def movement():
    if request.method == 'POST':
        from Test import buttonpitch
        move = request.get_json()
        if move != None:
            buttonpitch(True)
@app.route("/hold",methods=["POST"])
'''
@app.route("/stop",methods=['POST'])
def stopping():
    if request.method == 'POST':
        from Test import buttonhold
        buttonhold(True)
        return str(1)
if __name__ == "__main__":
    app.run()