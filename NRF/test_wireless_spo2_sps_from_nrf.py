import serial
import time
import datetime
from bokeh.plotting import figure, show
from bokeh.models import Span, Label

port = "/dev/ttyUSB3"
baudrate = 115200
print_each_frame = False
count_invalid_data = 0
frames_received_count = 0
invalid_samples_list = []


def read_nrf_msg(serial_port, timeout):
    def read_msg_till_footer(serial_port):
        msg = b''
        while True:
            data = serial_port.read()
            msg += data
            if data == b'\xAE':
                break
        return msg

    msg = b''
    start = time.time()
    while time.time() - start < timeout:
        data = serial_port.read()
        if data == b'\x3E':
            msg += data
            msg += read_msg_till_footer(serial_port)
            break
        elif data == b'':
            pass
        else:
            msg += data
            msg += serial_port.read(serial_port.in_waiting)
            print(f"Received some other msg \n{msg}")
            msg = b''

    return msg


def send_reset(serial_port):
    reset_msg = b"\x3E\x10\x04\x00\x00\x00\x54\x38\xCF\x9F\xAE"
    print("Sending RESET MSG to NRF")
    serial_port.write(reset_msg)
    wait_start = time.time()
    while time.time() - wait_start < 10:
        if serial_port.in_waiting > 0:
            t_taken = round(time.time() - wait_start, 3)
            print(f"Received data in {t_taken} seconds")
            data = read_nrf_msg(serial_port, 3)
            print(f"Received : {data}")
            byte_2 = [bytes([i]) for i in data]
            if byte_2[2] == b'\x01' and byte_2[3] == b'\x00':
                print("RESET --> SUCCESS")
                return True
    return False


def request_fw_version(serial_port):
    def get_version(data):
        version = b''
        for i in range(6, 14):
            version += data[i]
        return version

    req_fw_ver = b"\x3E\x10\x02\x00\x00\x00\x88\x67\xA4\xBA\xAE"
    print("Sending REQUEST FW MSG to NRF")
    serial_port.write(req_fw_ver)
    wait_start = time.time()
    while time.time() - wait_start < 3:
        if serial_port.in_waiting > 0:
            t_taken = round(time.time() - wait_start, 3)
            print(f"Received data in {t_taken} seconds")
            data = read_nrf_msg(serial_port, 3)
            print(f"Received : {data}")
            byte_arr = [bytes([i]) for i in data]
            if byte_arr[2] == b'\x02' and byte_arr[3] == b'\x00':
                print(f"FW VERSION : {get_version(byte_arr).decode()}")
                print("FW VERSION --> SUCCESS")
                return True
    return False


def send_rtc_time(serial_port):
    msg_rtc = b'\x3E\x10\x0A\x00\x04\x00\x0F\x4A\xAA\x66\x47\xE8\x8F\x2D\xAE '
    print("Sending RTC TIME to NRF")
    serial_port.write(msg_rtc)


def send_spo2_connect(serial_port):
    spo2_connect_msg = b'\x3E\x10\x01\xC1\x07\x00\x00\xA0\x50\x0C\x07\x2C\x00\xBD\xE1\xD4\x29\xAE'
    print("Sending SPO2 CONNECT MSG to NRF")
    serial_port.write(spo2_connect_msg)
    wait_start = time.time()
    while time.time() - wait_start < 10:
        if serial_port.in_waiting > 0:
            t_taken = round(time.time() - wait_start, 3)
            print(f"Received data in {t_taken} seconds")
            data = read_nrf_msg(serial_port, 3)
            print(f"Received : {data}")
            byte_arr = [bytes([i]) for i in data]
            if byte_arr[2] == b'\x81' and byte_arr[3] == b'\xC1':
                print("SPO2 CONNECT --> SUCCESS")
                return True
    return False


def process_spo2_data(data):
    global frames_received_count
    def process_frame(data_5b, index):
        global count_invalid_data
        if (int(data_5b[0]) & 1 != 1 and
            int(data_5b[1]) & 1 != 0 and
            int(data_5b[2]) & 1 != 0 and
            int(data_5b[3]) & 1 != 0 and
            int(data_5b[4]) & 1 != 0):
            print(f"INVALID DATA : SYNC BIT CHECK FAILED @{index:<3} --> {data_5b}")
            count_invalid_data += 1
            return 1
        if print_each_frame is True:
            finger_clipped = int(data_5b[2]) & (1 << 4)
            finger_clipped = 'CLIPPED' if finger_clipped == 0 else 'UNCLIPPED'
            signal_Strength = int(data_5b[0]) & (0xF)
            signal_Strength = 'INVALID' if signal_Strength == 0xF else signal_Strength
            probe_plugged = int(data_5b[0]) & (1 << 5)
            probe_plugged = 'PLUGGED' if probe_plugged == 0 else 'UNPLUGGED'
            hr_Data = (data_5b[3]) + (((data_5b[2]) & 0x40) << 1)
            hr_Data = 'INVALID' if hr_Data == 255 else hr_Data
            spo2_Data = int(data_5b[4])
            spo2_Data = 'INVALID' if spo2_Data == 127 else spo2_Data
            pleth = int(data_5b[1])
            pleth = 'INVALID' if pleth == 0 else pleth
            print(f"|{probe_plugged:^11}|{signal_Strength:^8}|{finger_clipped:^11}|{hr_Data:^9}|{spo2_Data:^9}|{pleth:^9}")
        return 0

    data_b = [bytes([i]) for i in data]
    for i in range(0, len(data_b)):
        data_b[i] = int.from_bytes(data_b[i], "little")
    # battery = data_b[10]
    # offset = data_b[11]
    if print_each_frame is True:
        print("Frame Info :-")
        print(f"|{'PROBE':^11}|{'SIGNAL':^8}|{'FINGER':^11}|{'HR':^9}|{'SPO2':^9}|{'Pleth':^9}")
    invalid_samples = 0
    for i in range(12, 512, 5):
        invalid_samples += process_frame(data_b[i:i+5], i)
        frames_received_count += 1
    print(f"Invalid Samples in 500B : {invalid_samples}")
    invalid_samples_list.append(invalid_samples)


def read_sensor_data(serial_port, duration):
    start = time.time()
    last_msg_rec = 0
    while time.time() - start < duration:
        if serial_port.in_waiting > 0:
            data = read_nrf_msg(serial_port, 5)
            # print(data)
            if last_msg_rec != 0:
                print(f"Time since last msg = {round(time.time() - last_msg_rec, 3):<5} ms | LEN : {len(data)}")
            last_msg_rec = time.time()
            process_spo2_data(data)
    invalid_percentage = round(count_invalid_data/frames_received_count*100, 2)
    print(f"Invalid Data Packets : {count_invalid_data}/{frames_received_count} {invalid_percentage} %")
    plot_invalid_samples(invalid_samples_list)
    print(invalid_samples_list)
    file = open("invalid_samples.txt", "w")
    file.write(str(invalid_samples_list))
    file.close()


def log_nrf_debug(serial_port, duration, filename):
    start = time.time()
    file = open(filename, "wb")
    while time.time() - start < duration:
        if serial_port.in_waiting > 0:
            data = serial_port.read(serial_port.in_waiting)
            print("Received --> ", data)
            file.write(data)
    file.close()


def plot_invalid_samples(inv_sample_list):
    p = figure(title="Invalid Sample count vs 500B frame index",
               width=1000, height=600)

# add a circle renderer with a size, color, and alpha
    p.scatter(list(range(len(inv_sample_list))), inv_sample_list, size=6, color="navy", alpha=0.5)
    p.yaxis.axis_label = "invalid_sample_count_in_500B"
    p.xaxis.axis_label = "500B Frame Index"

# show the results
    show(p)

if __name__=="__main__":
    nrf = serial.Serial(port, baudrate, timeout=0.1)

    nrf.reset_output_buffer()
    nrf.reset_input_buffer()

    # send_reset(nrf)
    # time.sleep(0.1)
    # request_fw_version(nrf)
    # time.sleep(0.1)
    # send_rtc_time(nrf)
    # time.sleep(2)
    # send_spo2_connect(nrf)
    time.sleep(2)
    read_sensor_data(nrf, 2 * 60)

    # now = str(datetime.datetime.now()).replace(" ", "_")
    # filename = "./nrf_debug_logs/" + now
    # log_nrf_debug(nrf, 30, filename)
    # data = process_nrf_debug_for_ble_notifications_spo2(filename)
    # check_sync_bits_of_spo2_data(data)
