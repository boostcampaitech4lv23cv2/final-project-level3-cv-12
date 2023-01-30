import io
import os
from pathlib import Path

import requests
from PIL import Image
import numpy as np

import streamlit as st


# SETTING PAGE CONFIG TO WIDE MODE
ASSETS_DIR_PATH = os.path.join(Path(__file__).parent.parent.parent.parent, "assets")


def main():
    st.title("Virtual Try-On - Cloth and Avatar")

    st.info("You need to upload cloth image and choose avatar", icon="💡")

    # 옷 타입, 아바타 타입 고르기
    col1, col2 = st.columns(2)
    with col1:
        cloth_type = st.radio(
            "Select cloth type.",
            ("dresses", "upper", "lower"),
            horizontal=True
        )
        st.write(f"You selected {cloth_type}")
    with col2:
        if cloth_type == "dresses":
            avatar_type = st.radio(
                "Select avatar type.",
                ("long", "short", "etc"),
                horizontal=True
            )
        elif cloth_type == "upper":
            avatar_type = st.radio(
                "Select avatar type.",
                ("long", "short", "sleeveless"),
                horizontal=True
            )
        elif cloth_type == "lower":
            avatar_type = st.radio(
                "Select avatar type.",
                ("long", "short", "skirt"),
                horizontal=True
            )
        st.write(f"You selected {avatar_type}")

    st.write("---")

    # cloth file upload
    files = list()
    uploaded_only_cloth_file = st.file_uploader(
        "Upload your cloth", 
        type=["jpg", "jpeg", "png"],
        key='only_cloth'
    )

    if uploaded_only_cloth_file:
        cloth_image_bytes = uploaded_only_cloth_file.getvalue()
        cloth_image = Image.open(io.BytesIO(cloth_image_bytes))
        files.append(
            (("cloth", (uploaded_only_cloth_file.name, cloth_image_bytes, 
                        uploaded_only_cloth_file.type)))
        )

    col1, col2 = st.columns(2)
    with col1:
        if uploaded_only_cloth_file:
            st.image(cloth_image.resize((384, 512)), caption="Cloth Image")
    with col2:
        avatar_image_path = f"{os.getcwd()}/app/sample_images/{cloth_type}/{avatar_type}/a.jpg"
        avatar_image = Image.open(avatar_image_path)
        st.image(avatar_image.resize((384, 512)), caption="Your Avatar")
        files.append(
            ("avatar_path", (avatar_image_path))
        )

    _, _, col_3, _, _= st.columns(5)
    with col_3:
        inference = st.button("Inference Button")

    _, col2, _ = st.columns([1.2, 3, 1])
    with col2:
        if inference:
            if uploaded_only_cloth_file:
                response = requests.post("http://localhost:8501/cloth-tryon", files=files)
                st.spinner("Wait for it ...")

                result_image = Image.open(io.BytesIO(response.content))
                st.image(result_image.resize((384, 512)), caption='Virtual Avatar')
            else:
                st.info("Please Upload Cloth", icon='🔥')

    _, col2, _ = st.columns([2.3, 3, 1])
    with col2:
        if inference:
            btn = st.download_button(
                    label="Download result image",
                    data=response.content,
                    file_name="result.jpg",
                    mime="image/jpg"
                )


if __name__ == '__main__':
    main()