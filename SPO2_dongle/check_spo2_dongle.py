import serial
import time
import datetime

ser = serial.Serial('/dev/ttyACM0', 230400, timeout=None)

ser.reset_output_buffer()
ser.reset_input_buffer()

counter = 0
new_time = 0

start = time.time()


while counter < 30:
    data_main = ser.read(500)
    for i in range(0, 100):
        data = data_main[i*5 : i*5 + 5]
        if (data[0] & (1 << 5)):
            probe = "DISCONN"
        else:
            probe = "CONN"
        if probe == "DISCONN":
            print(datetime.now(), hex(data[0]))
    counter += 1
