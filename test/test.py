import requests
import io
from PIL import Image
import json

URL = 'http://localhost:8501'

def test_post():
    cloth_byte_arr = io.BytesIO()
    cloth_image = Image.open('./test_cloth.jpg')
    cloth_image.save(cloth_byte_arr, format='PNG')
    human_byte_arr = io.BytesIO()
    human_image = Image.open('./test_avatar.jpg')
    human_image.save(human_byte_arr, format='PNG')
    files = [('part', 'upper'),('cloth', ('test_cloth.jpg', cloth_byte_arr.getvalue(), 'image/png')), ('human', ('test_avatar.jpg', human_byte_arr.getvalue(), 'image/png'))]
    response = requests.post(URL + "/all-tryon" , files=files)
    log = {"elapsed_time": response.elapsed.total_seconds()}
    with open('./result.jpg', 'wb') as f:
        f.write(response.content)
    with open('./elapsed_time.json', 'w') as f:
        json.dump(log, f)