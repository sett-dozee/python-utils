import serial
import time
import datetime
import math
import plotly.graph_objects as go
from itertools import count

ser = serial.Serial('/dev/ttyUSB0', 230400, timeout=None)

ser.reset_output_buffer()
ser.reset_input_buffer()

sheet1_start_bytes = 83, 72
sheet2_start_bytes = 85, 89
temperature_start_bytes = 84, 80
nibp_start_bytes = 51, 69
spo2_start_bytes = 79, 89

counter = 0
time.sleep(2)
ser.write(b'2')
ser.write(b'2')
time.sleep(0.2)
ser.write(b'b')
ser.write(b'b')
time.sleep(0.2)
ser.write(b'S')
ser.write(b'S')
time.sleep(0.2)
print("Sent start")
new_time = 0
sh1_f = open("SH1_MCP_SINE.pz", "wb")
sh2_f = open("SH2_MCP_SINE.pz", "wb")
raw_data_file = open("SPO2_RAW.txt", "wb")
file = open("Spo2_Raw.csv", "w")
file_d = open("Spo2_Debug.csv", "w")

x_vals = []
y_vals = []

index = count(0, 4)

start = time.time()

while True:
    data = ser.read(2)
    if data == b'':
        continue
    elif data == b'\xFF\xFE':
        print("Got debug")
        data = ser.read(8)
        file_d.write(f"DEBUG:{data}\n")
        print(data)
    elif data == b'SH':
        print(f"C={counter}")
        print("*****SH1*****")
        data_rec = ser.read(500)
        for data in data_rec:
            sh1_f.write(data.to_bytes(1, "big"))
        for i in range(0, len(data_rec), 2):
            bcg_val = (list(data_rec[i:i+2])[0] << 8) + \
                    list(data_rec[i:i+2])[1]
            if bcg_val < 300 or bcg_val > 700:
                print(i, index, bcg_val, data_rec[i:i+2])
            x_vals.append(next(index))
            y_vals.append(bcg_val)
        counter = 0
    elif data == b'TP':
        print(f"C={counter}")
        print("*****TEMP*****")
        counter = 0
    elif data == b'3E':
        print(f"C={counter}")
        print("*****NIBP*****")
        counter = 0
    elif data[0] >= 85 and data[0] < 89:
        print(f"C={counter}")
        print("*****SH2*****")
        data_rec = ser.read(510)
        for data in data_rec:
            sh2_f.write(data.to_bytes(1, "big"))
        counter = 0
    elif data == b'OY':
        print("*****SPO2*****")
        data_main = ser.read(500)

        elapsed = time.time() - new_time
        new_time = time.time()
        # print(f"Time to read = {end - start}")
        for i in range(0, 100):
            data = data_main[i*5:i*5+5]
            if (len(data) != 5):
                print(f"Received only {len(data)} bytes")
            if (data[0] & (1 << 5)):
                probe = "DISCONN"
            else:
                probe = "CONN"
            if (data[2] & (1 << 4)):
                finger = "UNCLIPPED"
            else:
                finger = "CLIPPED"

            pr = (data[3]) + ((data[2] & 0x40) << 1)
            spo2 = data[4]
            # print(f"RAW {i} : {hex(data[0])} {hex(data[1])} {hex(data[2])} {hex(data[3])} {hex(data[4])} | PROBE, FINGER : {probe, finger} | SPO2, PR : {spo2, pr}")
            file.write(f"{hex(data[0])},{hex(data[1])},{hex(data[2])},{hex(data[3])},{hex(data[4])}\n")
            raw_data_file.write(data[0].to_bytes(1, "big"))
            raw_data_file.write(data[1].to_bytes(1, "big"))
            raw_data_file.write(data[2].to_bytes(1, "big"))
            raw_data_file.write(data[3].to_bytes(1, "big"))
            raw_data_file.write(data[4].to_bytes(1, "big"))
            # if data[0] != 0x8f or data[1] != 0x0 or data[2] != 0x50 or data[3] != 0x7f or data[4] != 0x7f:
            #     print("Different value")

        print(f"Now = {datetime.datetime.now()}")
        print(f"Time elapsed since last SPO2 data chunk = {elapsed}")
        now = time.time()
        total_runtime_mins = math.floor((now - start) / 60)
        total_runtime_secs = round((now - start) % 60, 2)
        print(f"Total RunTime = {total_runtime_mins} mins {total_runtime_secs} secs")
        if elapsed > 1:
            print("Took longer than expected")
        counter = 0
    else:
        counter += 2
    if time.time() - start > 10:
        break

sh1_f.close()
sh2_f.close()
raw_data_file.close()
file.close()
file_d.close()

fig = go.Figure(data=go.Scatter(x=x_vals, y=y_vals,
                                line=dict(width=1),
                                connectgaps=True))
fig.show()
