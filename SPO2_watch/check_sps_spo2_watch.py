import asyncio
from bleak import BleakScanner, BleakClient
import time


async def discover_devices():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

address = "00:A0:50:0C:07:2C"
MODEL_NBR_UUID = "49535343-1e4d-4bd9-ba61-23c647249616"
last_received = 0
count_invalid_data = 0
total_samples = 0
count_invalid_sample_list = []


def callback(sender, data):
    global last_received
    global count_invalid_data
    global total_samples
    length = len([bytes([i]) for i in data])
    total_samples += length/5
    count_invalid_data = 0
    if length > 0:
        cur_received = time.time()
        print(length/5/(cur_received - last_received))
        last_received = cur_received
        for i in range(0, length, 5):
            data_5b = data[i:i+5]
            if (int(data_5b[0]) & 0x80 != 0x80 and
                int(data_5b[1]) & 0x80 != 0x00 and
                int(data_5b[2]) & 0x80 != 0x00 and
                int(data_5b[3]) & 0x80 != 0x00 and
                int(data_5b[4]) & 0x80 != 0x00):
                print(f"INVALID DATA : SYNC BIT CHECK FAILED @{i:<2} --> {data_5b}")
                count_invalid_data += 1
        count_invalid_sample_list.append([length, count_invalid_data])
        file.write(data)


async def connect_to_device_and_receive_data(address):
    async with BleakClient(address) as client:
        await client.start_notify(MODEL_NBR_UUID, callback)
        # time.sleep(2 * 60)
    total_samples_invalid = 0
    total_samples = 0
    for i in count_invalid_sample_list:
        total_samples_invalid += i[1]
        total_samples += i[0]
    print(total_samples_invalid, total_samples)
    percentage_err = total_samples_invalid/total_samples/5*100
    print(f"Total corrupt samples : {total_samples_invalid}/{total_samples} {percentage_err} %")

file = open("RAW_DATA_004.dat", "wb")
asyncio.run(connect_to_device_and_receive_data(address))
file.close()
