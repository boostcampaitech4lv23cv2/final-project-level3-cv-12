import requests
from PIL import Image
import io
import time
import os


def run_server():
    print(os.getcwd())
    time.sleep(5)
    print("warmup server start.")

    cloth = Image.open("service/back-end/warmup_sample/cloth.jpg")
    human = Image.open("service/back-end/warmup_sample/human.jpg")

    clothByteArr = io.BytesIO()
    cloth.save(clothByteArr, format=cloth.format)
    clothByteArr = clothByteArr.getvalue()

    humanByteArr = io.BytesIO()
    human.save(humanByteArr, format=human.format)
    humanByteArr = humanByteArr.getvalue()

    files = [
        ("part", ("dresses")),
        ("cloth", ("dummy", clothByteArr, "image/jpeg")),
        ("human", ("dummy", humanByteArr, "image/jpeg")),
    ]

    response = requests.post("http://0.0.0.0:8501/all-tryon", files=files)

    if response.status_code == 200:
        print("completed warmup.")
    else:
        print(f"{response.status_code} error occurred while warmup.")


run_server()
