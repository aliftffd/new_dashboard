# rfid_reader.py

import serial
import time
import threading
from datetime import datetime

class RFIDReader:
    def __init__(self, port, baud_rate, callback):
        self.serial_port = serial.Serial(port, baud_rate)
        self.stop_event = threading.Event()
        self.callback = callback
        self.tag_status = "Stand By ..."
        self.thread = threading.Thread(target=self.read_tag)
        self.thread.start()

    def read_tag(self):
        tag_names = {
            b'\xE2\x00\x20\x23\x12\x05\xEE\xAA\x00\x01\x00\x73': "TAG 1",
            b'\xE2\x00\x20\x23\x12\x05\xEE\xAA\x00\x01\x00\x76': "TAG 2",
            b'\xE2\x00\x20\x23\x12\x05\xEE\xAA\x00\x01\x00\x90': "TAG 3",
            b'\xE2\x00\x20\x23\x12\x05\xEE\xAA\x00\x01\x00\x87': "TAG 4",
            b'\xE2\x00\x20\x23\x12\x05\xEE\xAA\x00\x01\x00\x88': "TAG 5"
        }

        while not self.stop_event.is_set():
            command = b'\x43\x4D\x02\x02\x00\x00\x00\x00'
            self.serial_port.write(command)
            data = self.serial_port.read(26)

            if data:
                tag_detected = False
                for tag, name in tag_names.items():
                    if data.startswith(tag):
                        tag_detected = True
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        formatted_tag = self.format_tag_id(tag)
                        print(f"{name} detected: {formatted_tag} at {timestamp}")
                        self.tag_status = name
                        self.callback(name, formatted_tag, timestamp)
                        break
                if not tag_detected:
                    self.tag_status = "STAND BY ..."
            else:
                self.tag_status = "STAND BY ..."
            time.sleep(1)

    @staticmethod
    def format_tag_id(tag):
        return '-'.join(f"{byte:02X}" for byte in tag)

    def stop(self):
        self.stop_event.set()
        self.thread.join()

if __name__ == "__main__":
    def rfid_callback(name, tag_id, timestamp):
        print(f"RFID Callback - Timestamp: {timestamp}, Name: {name}, Tag ID: {tag_id}")

    rfid_reader = RFIDReader(port='/dev/...', baud_rate=115200, callback=rfid_callback)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        rfid_reader.stop()
