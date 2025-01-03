import datetime as dt
import json
import requests

key = "daq0:Q0bGUVEoCrUFbuCXcM6c"


def check_fsr(device_id):
    url = f"https://daq.dozee.cloud/api/devices/0/{device_id}/fsr/get"
    headers = {'x-api-key': f'{key}'}

    response = requests.request('GET',
                                url=url,
                                headers=headers,
                                timeout=5)
    return response

def update_fsr(device_id, baseline, delta):
    url = f"https://daq.dozee.cloud/api/devices/0/{device_id}/fsr/update"
    headers = {'x-api-key': f'{key}'}

    payload = {
            "OccupancyFsrBaseline": baseline,
            "OccupancyFsrDelta": delta
    }

    response = requests.request('POST',
                                url=url,
                                headers=headers,
                                data=json.dumps(payload),
                                timeout=5)
    return response


fsr_baseline = 600
fsr_delta = 400
device_id = "d939152d-3a12-46e6-8af9-e7f833c2b62a"

response = update_fsr(device_id, fsr_baseline, fsr_delta)
print(response.text)
response = check_fsr(device_id)
print(response.text)
