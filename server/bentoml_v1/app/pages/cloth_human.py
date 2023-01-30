import io
import os
from pathlib import Path

import requests
from PIL import Image

import streamlit as st


# SETTING PAGE CONFIG TO WIDE MODE
ASSETS_DIR_PATH = os.path.join(Path(__file__).parent.parent.parent.parent, "assets")


def main():
    st.title("Virtual Try-On - Cloth and Human")

    st.info("You need to upload cloth and body image", icon="💡")

    cloth_type = st.radio(
        "Select cloth type.",
        ("dresses", "upper", "lower"),
        horizontal=True
    )
    st.write(f"You selected {cloth_type}")

    st.write("---")

    files = list()
    files.append(
        ('part', (cloth_type))
    )

    col1, col2 = st.columns(2)
    with col1:
        uploaded_cloth_file = st.file_uploader(
            "Upload your cloth", 
            type=["jpg", "jpeg", "png"],
            key='cloth'
        )

        if uploaded_cloth_file:
            cloth_image_bytes = uploaded_cloth_file.getvalue()
            cloth_image = Image.open(io.BytesIO(cloth_image_bytes))
            st.image(cloth_image.resize((384, 512)), caption='Cloth Image')
            files.append(
                ("cloth", (uploaded_cloth_file.name, cloth_image_bytes, 
                           uploaded_cloth_file.type))
            )

    with col2:
        uploaded_human_file = st.file_uploader(
            "Upload your body", 
            type=["jpg", "jpeg", "png"],
            key='body'
        )

        if uploaded_human_file:
            human_image_bytes = uploaded_human_file.getvalue()
            human_image = Image.open(io.BytesIO(human_image_bytes))
            st.image(human_image.resize((384, 512)), caption="Your Avatar")
            files.append(
                ("human", (uploaded_human_file.name, human_image_bytes, 
                           uploaded_human_file.type))
            )

    _, _, col_3, _, _= st.columns(5)
    with col_3:
        inference = st.button("Inference Button")
        
    _, col2, _ = st.columns([1.2, 3, 1])
    with col2:
        if inference:
            if uploaded_cloth_file and uploaded_human_file:
                with st.spinner("Wait for it …"):
                    response = requests.post("http://localhost:8501/all-tryon", files=files)
                
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