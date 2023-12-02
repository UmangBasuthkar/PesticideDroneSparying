from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__, static_folder='static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

data = []

@app.route('/')
def index():
    return render_template("main.html")

@app.route('/startMission')
def startmission():
    return render_template("Test.html")

@app.route('/', methods=['POST'])
def location_data():
    if request.method == 'POST':
        received_data = request.get_json()
        data.extend(received_data)
    return "Data received successfully"  # Return a response to acknowledge data reception

@app.route('/details', methods=['GET'])
def details():
    return render_template('parameters.html')

@app.route('/process_data', methods=['POST'])
def process_data():
    if request.method == 'POST':
        d1 = request.json
        quantity = d1['data1']
        altitude = d1['data2']
        from RunCommand import command
        command(str(data[0]['lat']), str(data[0]['lng']))
        time.sleep(8)
        from Test import fly
        fly(data,float(altitude), float(20.0), float(3.0))
        return str(quantity)

if __name__ == "__main__":
    app.run(host="localhost", port=9999, debug=True)
