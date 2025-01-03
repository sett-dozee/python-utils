import serial
import time
import datetime

ser = serial.Serial('/dev/ttyUSB1', 9600, timeout=None)

ser.reset_output_buffer()
ser.reset_input_buffer()

counter = 0
new_time = 0

old_send_time = 0

f = open("SPO2_RAW.txt", "rb")

while True:
    data = f.read(5)
    if data == b'':
        f.seek(0)
        continue
    # send data
    while time.time() - old_send_time < 0.01:
        continue
    ser.write(data)
    old_time = time.time()
    print(data)
    counter += 1
