import serial
import time

sh1 = serial.Serial('/dev/ttyUSB1', 115200, timeout=None)
sh2 = serial.Serial('/dev/ttyUSB2', 115200, timeout=None)

sh1.reset_output_buffer()
sh2.reset_output_buffer()
sh2.reset_input_buffer()
sh2.reset_input_buffer()

sheet1_start_bytes = 83, 72
sheet2_start_bytes = 85, 89
temperature_start_bytes = 84, 80
nibp_start_bytes = 51, 69
spo2_start_bytes = 79, 89

counter = 0
sh1.write(b'4')
sh2.write(b'4')
time.sleep(0.2)
sh1.write(b'b')
sh2.write(b'b')
time.sleep(0.2)
sh1.write(b'S')
sh2.write(b'S')
time.sleep(0.2)
print("Sent start")
new_time = 0
# sh1_f = open("SH1_TEST.pz", "wb")
# sh2_f = open("SH2_TEST.pz", "wb")

start = time.time()
sec_counter = time.time()

byte_loss = False
count = 0
total = 0
# fsr_list = []
# fsr_raw_1 = []
# fsr_raw_2 = []

while True:
    data_sh1 = sh1.read(2)
    data_sh2 = sh2.read(2)
    if len(data_sh2) < 2:
        break
    if data_sh2[0] > 3:  # Maybe have received an FSR sample
        if data_sh2[0] > 83 or data_sh2[0] < 80:  # Definitely byte loss
            if byte_loss is False:
                byte_loss = True
                count += 1
                # print(f"{hex(data_sh2[0])}, {hex(data_sh2[1])}")
        elif byte_loss is True:
            byte_loss = True
            fsr = ((data_sh2[0] - 80) << 8) + data_sh2[1]
            # fsr_list.append(fsr)
            # fsr_raw_1.append([data_sh2[0], data_sh2[1], total])
            if fsr < 600:
                print(f"@BL FSR : {data_sh2[0]:<2}, {data_sh2[1]}")
        else:  # Received an FSR sample
            # print(f"@NL FSR : {data_sh2[0]:<2}, {data_sh2[1]}")
            fsr = ((data_sh2[0] - 80) << 8) + data_sh2[1]
            # fsr_list.append(((data_sh2[0] - 80) << 8) + data_sh2[1])
            # fsr_raw_2.append([data_sh2[0], data_sh2[1], total])
            if fsr < 600:
                print(f"@NL FSR : {data_sh2[0]:<2}, {data_sh2[1]}")
    elif byte_loss is True:  # Received a piezo sample
        byte_loss = False
    # sh1_f.write(data_sh1)
    # sh2_f.write(data_sh2)

    if time.time() - sec_counter > 15:
        sec_counter = time.time()
        elapsed = time.time() - start
        mins = int(elapsed / 60)
        secs = int(elapsed % 60)
        print(f"Elapsed : {mins:>3}m {secs:>2}s")

    if time.time() - start > 5 * 60:
        break

# sh1_f.close()
# sh2_f.close()
