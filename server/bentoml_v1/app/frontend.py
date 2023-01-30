import io
import os
from pathlib import Path

import numpy as np

import requests
from PIL import Image

import streamlit as st
from app.confirm_button_hack import cache_on_button_press

import torch

# SETTING PAGE CONFIG TO WIDE MODE
ASSETS_DIR_PATH = os.path.join(Path(__file__).parent.parent.parent.parent, "assets")

st.set_page_config(layout="wide")

root_password = 'password'

def main():
    st.title("Virtual Try-On Test")
    uploaded_cloth_file = st.file_uploader("Choose an cloth image", type=["jpg", "jpeg", "png"])
    uploaded_human_file = st.file_uploader("Choose an human image", type=["jpg", "jpeg", "png"])

    if uploaded_cloth_file and uploaded_human_file:
        cloth_bytes = uploaded_cloth_file.getvalue()
        cloth_image = Image.open(io.BytesIO(cloth_bytes))

        human_bytes = uploaded_human_file.getvalue()
        human_image = Image.open(io.BytesIO(human_bytes))
        
        st.image(cloth_image.resize((256,192)), caption='Uploaded Image')
        st.image(human_image.resize((256,192)), caption='Uploaded Image')
        st.write("Making avatar ...")
        
        files = [
            ('cloth', (uploaded_cloth_file.name, cloth_bytes,
                       uploaded_cloth_file.type)),
            ('human', (uploaded_human_file.name, human_bytes,
                       uploaded_human_file.type))
        ]
        
        response = requests.post("http://localhost:8501/all-tryon", files=files)   
        result_image = Image.open(io.BytesIO(response.content))

        st.image(result_image, caption='Virtual Avatar')

@cache_on_button_press('Authenticate')
def authenticate(password) -> bool:
    return password == root_password

password = st.text_input('password', type="password")

if authenticate(password):
    st.success('You are authenticated!')
    main()
else:
    st.error('The password is invalid.')
