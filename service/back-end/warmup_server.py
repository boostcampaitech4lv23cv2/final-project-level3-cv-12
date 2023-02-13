import requests
from PIL import Image
import io
import time

def run_server():
    time.sleep(5)
    print("warmup server start.")

    cloth = Image.open("service/back-end/sample_images/warmup_sample/cloth.jpg").convert('RGB').resize((768, 1024))
    human = Image.open("service/back-end/sample_images/warmup_sample/human.jpg").convert('RGB').resize((768, 1024))

    clothByteArr = io.BytesIO()
    cloth.save(clothByteArr, format='JPEG')
    clothByteArr = clothByteArr.getvalue()

    humanByteArr = io.BytesIO()
    human.save(humanByteArr, format='JPEG')
    humanByteArr = humanByteArr.getvalue()

    files = [
        ("part", ("upper")),
        ("cloth", ("dummy", clothByteArr, "image/jpeg")),
        ("human", ("dummy", humanByteArr, "image/jpeg")),
    ]

    response = requests.post("http://0.0.0.0:8501/all-tryon", files=files)

    if response.status_code == 200:
        print("completed warmup.")
    else:
        print(f"{response.status_code} error occurred while warmup.")

run_server()