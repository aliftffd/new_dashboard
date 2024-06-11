# app.py
import json
import threading
import logging
from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
from datetime import datetime
from time import sleep
from speed_reader import Readspeed
from rfid_reader import RFIDReader

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Bissmillah!'
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app, origins=["http://localhost:5173"])

# Shared data structure
shared_data = {
    'timestamp': None,
    'value': None,
    'Tag': None,
    'ID': None
}

# Thread lock for synchronizing access to shared data
thread_lock = Lock()

# Initialize speed reader and RFID reader
readspeed = Readspeed('/dev/ttyUSB0', 195200)
rfidreader = RFIDReader('/dev/ttyUSB1', 115200, callback=lambda name, tag_id, timestamp: rfid_callback(name, tag_id, timestamp))

def get_current_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def speed_callback(speed):
    with thread_lock:
        shared_data['value'] = speed
        shared_data['timestamp'] = get_current_datetime()
        logging.info(f"Speed Data: {shared_data}")
        socketio.emit('sensorData', json.dumps(shared_data))

def rfid_callback(name, tag_id, timestamp):
    with thread_lock:
        shared_data['Tag'] = name
        shared_data['ID'] = tag_id
        shared_data['timestamp'] = timestamp
        logging.info(f"RFID Data: {shared_data}")
        socketio.emit('sensorData', json.dumps(shared_data))

# Start the speed reader and RFID reader in separate threads
def start_sensors():
    threading.Thread(target=readspeed.start_reading, args=(speed_callback,)).start()
    threading.Thread(target=rfidreader.read_tag).start()

@app.route('/')
def index():
    return "RFID and Speed Reader Server Running"

if __name__ == "__main__":
    start_sensors()
    try:
        socketio.run(app, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        rfidreader.stop()
        readspeed.stop()
        logging.info("Server stopped.")
