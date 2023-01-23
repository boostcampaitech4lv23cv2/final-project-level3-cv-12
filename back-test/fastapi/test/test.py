import requests
import io
from PIL import Image
import json

URL = 'http://www.localhost:8001'

def test_post():
    files = {'files': open('./assets/daflow/test_cloth.jpg', 'rb')}
    response = requests.post(URL + "/order" , files=files)
    log = {"elapsed_time": response.elapsed.total_seconds()}
    with open('./result.jpg', 'wb') as f:
        f.write(response.content)
    with open('./elapsed_time.json', 'w') as f:
        json.dump(log, f)
