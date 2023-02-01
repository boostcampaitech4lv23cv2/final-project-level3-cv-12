import io
import os
from pathlib import Path

import requests
from PIL import Image
import numpy as np

import streamlit as st

from pages.utils.check import *


# SETTING PAGE CONFIG TO WIDE MODE
ASSETS_DIR_PATH = os.path.join(Path(__file__).parent.parent.parent.parent, "assets")

if 'dress' not in st.session_state:
    st.session_state.dress = 0
    st.session_state.upper = 0
    st.session_state.lower = 0

if "dress_long" not in st.session_state:
    st.session_state.dress_long = 0
    st.session_state.dress_short = 0
    st.session_state.dress_etc = 0

    st.session_state.upper_long = 0
    st.session_state.upper_short = 0
    st.session_state.upper_etc = 0

    st.session_state.lower_long = 0
    st.session_state.lower_short = 0
    st.session_state.lower_etc = 0

if "Woman_a" not in st.session_state:
    st.session_state.Woman_a = 0
    st.session_state.Woman_b = 0
    st.session_state.Woman_c = 0
    st.session_state.Woman_d = 0
    st.session_state.Woman_e = 0

if "Man_a" not in st.session_state:
    st.session_state.Man_a = 0
    st.session_state.Man_b = 0
    st.session_state.Man_c = 0
    st.session_state.Man_d = 0
    st.session_state.Man_e = 0


def main():
    st.title("Virtual Try-On - Cloth and Avatar")

    st.info("You need to upload cloth image and choose avatar", icon="💡")

    # 옷 타입, 아바타 타입 고르기
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("대분류를 골라주세요")
        dress = st.checkbox("Dress", value=st.session_state.dress, on_change=check_dress)
        upper = st.checkbox("Upper", value=st.session_state.upper, on_change=check_upper)
        lower = st.checkbox("Lower", value=st.session_state.lower, on_change=check_lower)
    with col2:
        if dress:
            st.write("소분류를 골라주세요")
            dress_long = st.checkbox("long", value=st.session_state.dress_long, on_change=check_dress_long)
            dress_short = st.checkbox("short", value=st.session_state.dress_short, on_change=check_dress_short)
            dress_etc = st.checkbox("etc", value=st.session_state.dress_etc, on_change=check_dress_etc)
        elif upper:
            st.write("소분류를 골라주세요")
            upper_long = st.checkbox("long", value=st.session_state.upper_long, on_change=check_upper_long)
            upper_short = st.checkbox("short", value=st.session_state.upper_short, on_change=check_upper_short)
            upper_etc = st.checkbox("etc",value=st.session_state.upper_etc, on_change=check_upper_etc)
        elif lower:
            st.write("소분류를 골라주세요")
            lower_long = st.checkbox("long", value=st.session_state.lower_long, on_change=check_lower_long)
            lower_short = st.checkbox("short", value=st.session_state.lower_short, on_change=check_lower_short)
            lower_etc = st.checkbox("etc", value=st.session_state.lower_etc, on_change=check_lower_etc)
    with col3:
        if st.session_state.dress_long:
            st.write("아바타를 골라주세요")
            Woman_a = st.checkbox("Woman_a", value=st.session_state.Woman_a, on_change=check_woman_one)
            Woman_b = st.checkbox("Woman_b", value=st.session_state.Woman_b, on_change=check_woman_two)
            Woman_c = st.checkbox("Woman_c", value=st.session_state.Woman_c, on_change=check_woman_three)
            Woman_d = st.checkbox("Woman_d", value=st.session_state.Woman_d, on_change=check_woman_four)
            Woman_e = st.checkbox("Woman_e", value=st.session_state.Woman_e, on_change=check_woman_five)
        elif st.session_state.dress_short:
            st.write("아바타를 골라주세요")
            Woman_a = st.checkbox("Woman_a", value=st.session_state.Woman_a, on_change=check_woman_one)
            Woman_b = st.checkbox("Woman_b", value=st.session_state.Woman_b, on_change=check_woman_two)
            Woman_c = st.checkbox("Woman_c", value=st.session_state.Woman_c, on_change=check_woman_three)
            Woman_d = st.checkbox("Woman_d", value=st.session_state.Woman_d, on_change=check_woman_four)
            Woman_e = st.checkbox("Woman_e", value=st.session_state.Woman_e, on_change=check_woman_five)
        elif st.session_state.dress_etc:
            st.write("아바타를 골라주세요")
            Woman_a = st.checkbox("Woman_a", value=st.session_state.Woman_a, on_change=check_woman_one)
            Woman_b = st.checkbox("Woman_b", value=st.session_state.Woman_b, on_change=check_woman_two)
            Woman_c = st.checkbox("Woman_c", value=st.session_state.Woman_c, on_change=check_woman_three)
            Woman_d = st.checkbox("Woman_d", value=st.session_state.Woman_d, on_change=check_woman_four)
            Woman_e = st.checkbox("Woman_e", value=st.session_state.Woman_e, on_change=check_woman_five)
        elif st.session_state.upper_long:
            st.write("아바타를 골라주세요")
            Woman_a = st.checkbox("Woman_a", value=st.session_state.Woman_a, on_change=check_woman_one)
            Woman_b = st.checkbox("Woman_b", value=st.session_state.Woman_b, on_change=check_woman_two)
            Woman_c = st.checkbox("Woman_c", value=st.session_state.Woman_c, on_change=check_woman_three)
            Woman_d = st.checkbox("Woman_d", value=st.session_state.Woman_d, on_change=check_woman_four)
            Woman_e = st.checkbox("Woman_e", value=st.session_state.Woman_e, on_change=check_woman_five)
            Man_a = st.checkbox("Man_a", value=st.session_state.Man_a, on_change=check_man_one)
            Man_b = st.checkbox("Man_b", value=st.session_state.Man_b, on_change=check_man_two)
            Man_c = st.checkbox("Man_c", value=st.session_state.Man_c, on_change=check_man_three)
            Man_d = st.checkbox("Man_d", value=st.session_state.Man_d, on_change=check_man_four)
            Man_e = st.checkbox("Man_e", value=st.session_state.Man_e, on_change=check_man_five)
        elif st.session_state.upper_short:
            st.write("아바타를 골라주세요")
            Woman_a = st.checkbox("Woman_a", value=st.session_state.Woman_a, on_change=check_woman_one)
            Woman_b = st.checkbox("Woman_b", value=st.session_state.Woman_b, on_change=check_woman_two)
            Woman_c = st.checkbox("Woman_c", value=st.session_state.Woman_c, on_change=check_woman_three)
            Woman_d = st.checkbox("Woman_d", value=st.session_state.Woman_d, on_change=check_woman_four)
            Woman_e = st.checkbox("Woman_e", value=st.session_state.Woman_e, on_change=check_woman_five)
            Man_a = st.checkbox("Man_a", value=st.session_state.Man_a, on_change=check_man_one)
            Man_b = st.checkbox("Man_b", value=st.session_state.Man_b, on_change=check_man_two)
            Man_c = st.checkbox("Man_c", value=st.session_state.Man_c, on_change=check_man_three)
            Man_d = st.checkbox("Man_d", value=st.session_state.Man_d, on_change=check_man_four)
            Man_e = st.checkbox("Man_e", value=st.session_state.Man_e, on_change=check_man_five)
        elif st.session_state.upper_etc:
            st.write("아바타를 골라주세요")
            Woman_a = st.checkbox("Woman_a", value=st.session_state.Woman_a, on_change=check_woman_one)
            Woman_b = st.checkbox("Woman_b", value=st.session_state.Woman_b, on_change=check_woman_two)
            Woman_c = st.checkbox("Woman_c", value=st.session_state.Woman_c, on_change=check_woman_three)
            Woman_d = st.checkbox("Woman_d", value=st.session_state.Woman_d, on_change=check_woman_four)
            Woman_e = st.checkbox("Woman_e", value=st.session_state.Woman_e, on_change=check_woman_five)
            Man_a = st.checkbox("Man_a", value=st.session_state.Man_a, on_change=check_man_one)
            Man_b = st.checkbox("Man_b", value=st.session_state.Man_b, on_change=check_man_two)
            Man_c = st.checkbox("Man_c", value=st.session_state.Man_c, on_change=check_man_three)
            Man_d = st.checkbox("Man_d", value=st.session_state.Man_d, on_change=check_man_four)
            Man_e = st.checkbox("Man_e", value=st.session_state.Man_e, on_change=check_man_five)
        elif st.session_state.lower_long:
            st.write("아바타를 골라주세요")
            Woman_a = st.checkbox("Woman_a", value=st.session_state.Woman_a, on_change=check_woman_one)
            Woman_b = st.checkbox("Woman_b", value=st.session_state.Woman_b, on_change=check_woman_two)
            Woman_c = st.checkbox("Woman_c", value=st.session_state.Woman_c, on_change=check_woman_three)
            Woman_d = st.checkbox("Woman_d", value=st.session_state.Woman_d, on_change=check_woman_four)
            Woman_e = st.checkbox("Woman_e", value=st.session_state.Woman_e, on_change=check_woman_five)
            Man_a = st.checkbox("Man_a", value=st.session_state.Man_a, on_change=check_man_one)
            Man_b = st.checkbox("Man_b", value=st.session_state.Man_b, on_change=check_man_two)
            Man_c = st.checkbox("Man_c", value=st.session_state.Man_c, on_change=check_man_three)
            Man_d = st.checkbox("Man_d", value=st.session_state.Man_d, on_change=check_man_four)
            Man_e = st.checkbox("Man_e", value=st.session_state.Man_e, on_change=check_man_five)
        elif st.session_state.lower_short:
            st.write("아바타를 골라주세요")
            Woman_a = st.checkbox("Woman_a", value=st.session_state.Woman_a, on_change=check_woman_one)
            Woman_b = st.checkbox("Woman_b", value=st.session_state.Woman_b, on_change=check_woman_two)
            Woman_c = st.checkbox("Woman_c", value=st.session_state.Woman_c, on_change=check_woman_three)
            Woman_d = st.checkbox("Woman_d", value=st.session_state.Woman_d, on_change=check_woman_four)
            Woman_e = st.checkbox("Woman_e", value=st.session_state.Woman_e, on_change=check_woman_five)
            Man_a = st.checkbox("Man_a", value=st.session_state.Man_a, on_change=check_man_one)
            Man_b = st.checkbox("Man_b", value=st.session_state.Man_b, on_change=check_man_two)
            Man_c = st.checkbox("Man_c", value=st.session_state.Man_c, on_change=check_man_three)
            Man_d = st.checkbox("Man_d", value=st.session_state.Man_d, on_change=check_man_four)
            Man_e = st.checkbox("Man_e", value=st.session_state.Man_e, on_change=check_man_five)
        elif st.session_state.lower_etc:
            st.write("아바타를 골라주세요")
            Woman_a = st.checkbox("Woman_a", value=st.session_state.Woman_a, on_change=check_woman_one)
            Woman_b = st.checkbox("Woman_b", value=st.session_state.Woman_b, on_change=check_woman_two)
            Woman_c = st.checkbox("Woman_c", value=st.session_state.Woman_c, on_change=check_woman_three)
            Woman_d = st.checkbox("Woman_d", value=st.session_state.Woman_d, on_change=check_woman_four)
            Woman_e = st.checkbox("Woman_e", value=st.session_state.Woman_e, on_change=check_woman_five)
            Man_a = st.checkbox("Man_a", value=st.session_state.Man_a, on_change=check_man_one)
            Man_b = st.checkbox("Man_b", value=st.session_state.Man_b, on_change=check_man_two)
            Man_c = st.checkbox("Man_c", value=st.session_state.Man_c, on_change=check_man_three)
            Man_d = st.checkbox("Man_d", value=st.session_state.Man_d, on_change=check_man_four)
            Man_e = st.checkbox("Man_e", value=st.session_state.Man_e, on_change=check_man_five)

        image_path = list()
        for key in sorted(st.session_state):
            if st.session_state[key]:
                image_path.append(key)

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
        cloth_image = Image.open(io.BytesIO(cloth_image_bytes)).resize((384, 512))
        
        cloth_image_byte_arr = io.BytesIO()
        cloth_image.save(cloth_image_byte_arr, format='PNG')
        cloth_image_bytes = cloth_image_byte_arr.getvalue()
        
        files.append(
            (("cloth", (uploaded_only_cloth_file.name, cloth_image_bytes, 
                        uploaded_only_cloth_file.type)))
        )

    col1, col2 = st.columns(2)
    with col1:
        if uploaded_only_cloth_file:
            st.image(cloth_image.resize((384, 512)), caption="Cloth Image")
    with col2:
        if len(image_path) == 3:
            avatar_image_path = f"{os.getcwd()}/app/sample_images/{image_path[1]}/{image_path[2].split('_')[1]}/{image_path[0]}.jpg"
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
                with st.spinner("Wait for it …"):
                    response = requests.post("http://localhost:8501/cloth-tryon", files=files)

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