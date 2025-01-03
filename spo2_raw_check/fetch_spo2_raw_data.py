import datetime as dt
import json
import requests

key = "TnxV3x7XOku8T1y4Zqvb"
def get_download_link(device_id,start_time,end_time,emails):
    url = "https://console.senslabs.io/api/rawfiles/request" 
    headers = {'x-api-key':f'{key}'}

    payload = {
      "DeviceId": device_id,
      "From": (dt.datetime.fromisoformat(start_time)-dt.timedelta(hours=5.5)).isoformat(),
      "To": (dt.datetime.fromisoformat(end_time)-dt.timedelta(hours=5.5)).isoformat(),
      "Emails": emails
    }
    
    response = requests.post(url=url, headers=headers, data= json.dumps(payload), timeout=10)
#     print(json.dumps(payload))
    print(response)
    return response

device_id="83ca35ba-26ea-4748-a56f-ff0d935799ac"
start_time="2024-04-04 15:30:00"
end_time="2024-04-05 05:30:00"

emails = "deepsett@dozee.io"

response = get_download_link(device_id,start_time,end_time,emails)
print(response)
