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

if "dress" not in st.session_state:
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

    st.session_state.lower_pantslong = 0
    st.session_state.lower_pantsshort = 0
    st.session_state.lower_skirtlong = 0
    st.session_state.lower_skirtshort = 0

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


def write_category_main():
    st.write("###### 대분류")


def write_category_sub():
    st.write("###### 소분류")


def write_category_avatar():
    st.write("###### 모델")


def main():
    dir_root = os.getcwd()

    _, col, _ = st.columns([1.3, 3.2, 1])
    with col:
        st.title("의류 가상 피팅 서비스")
    _, col, _ = st.columns([1, 1.3, 1])
    with col:
        st.write("### 제공된 모델 활용하기")
    for _ in range(3):
        st.write("")

    # guide
    guide = st.checkbox("권장 사항", key="zz_guide_1")
    if guide:
        st.info(
            """
            옷은 겹쳐서 가려지는 부분이 없는 사진을 업로드 해주세요. \n
            입을 옷과 유사한 형태의 옷을 입은 모델을 선택하는 것을 권장합니다.
            """
        )

    # 옷 타입, 아바타 타입 고르기

    st.write("##### ✔ 입을 옷 유형과 모델 사진을 선택해 주세요.")
    st.write("")

    col1, col2, col3 = st.columns(3)
    with col1:
        write_category_main()
        dress = st.checkbox("드레스", value=st.session_state.dress, on_change=check_dress)
        upper = st.checkbox("상의", value=st.session_state.upper, on_change=check_upper)
        lower = st.checkbox("하의", value=st.session_state.lower, on_change=check_lower)
    with col2:
        if dress:
            write_category_sub()
            dress_long = st.checkbox(
                "긴소매", value=st.session_state.dress_long, on_change=check_dress_long
            )
            dress_short = st.checkbox(
                "반소매", value=st.session_state.dress_short, on_change=check_dress_short
            )
            dress_etc = st.checkbox(
                "민소매", value=st.session_state.dress_etc, on_change=check_dress_etc
            )
        elif upper:
            write_category_sub()
            upper_long = st.checkbox(
                "긴소매", value=st.session_state.upper_long, on_change=check_upper_long
            )
            upper_short = st.checkbox(
                "반소매", value=st.session_state.upper_short, on_change=check_upper_short
            )
            upper_etc = st.checkbox(
                "민소매", value=st.session_state.upper_etc, on_change=check_upper_etc
            )
        elif lower:
            write_category_sub()
            lower_pantslong = st.checkbox(
                "긴 바지",
                value=st.session_state.lower_pantslong,
                on_change=check_lower_pants_long,
            )
            lower_pantsshort = st.checkbox(
                "짧은 바지",
                value=st.session_state.lower_pantsshort,
                on_change=check_lower_pants_short,
            )
            lower_skirtlong = st.checkbox(
                "긴 치마",
                value=st.session_state.lower_skirtlong,
                on_change=check_lower_skirt_long,
            )
            lower_skirtshort = st.checkbox(
                "짧은 치마",
                value=st.session_state.lower_skirtshort,
                on_change=check_lower_skirt_short,
            )
    with col3:
        if st.session_state.dress_long:
            write_category_avatar()
            Woman_a = st.checkbox(
                "여 1", value=st.session_state.Woman_a, on_change=check_woman_one
            )
            Woman_b = st.checkbox(
                "여 2", value=st.session_state.Woman_b, on_change=check_woman_two
            )
            Woman_c = st.checkbox(
                "여 3", value=st.session_state.Woman_c, on_change=check_woman_three
            )
            Woman_d = st.checkbox(
                "여 4", value=st.session_state.Woman_d, on_change=check_woman_four
            )
            Woman_e = st.checkbox(
                "여 5", value=st.session_state.Woman_e, on_change=check_woman_five
            )
        elif st.session_state.dress_short:
            write_category_avatar()
            Woman_a = st.checkbox(
                "여 1", value=st.session_state.Woman_a, on_change=check_woman_one
            )
            Woman_b = st.checkbox(
                "여 2", value=st.session_state.Woman_b, on_change=check_woman_two
            )
            Woman_c = st.checkbox(
                "여 3", value=st.session_state.Woman_c, on_change=check_woman_three
            )
            Woman_d = st.checkbox(
                "여 4", value=st.session_state.Woman_d, on_change=check_woman_four
            )
            Woman_e = st.checkbox(
                "여 5", value=st.session_state.Woman_e, on_change=check_woman_five
            )
        elif st.session_state.dress_etc:
            write_category_avatar()
            Woman_a = st.checkbox(
                "여 1", value=st.session_state.Woman_a, on_change=check_woman_one
            )
            Woman_b = st.checkbox(
                "여 2", value=st.session_state.Woman_b, on_change=check_woman_two
            )
            Woman_c = st.checkbox(
                "여 3", value=st.session_state.Woman_c, on_change=check_woman_three
            )
            Woman_d = st.checkbox(
                "여 4", value=st.session_state.Woman_d, on_change=check_woman_four
            )
            Woman_e = st.checkbox(
                "여 5", value=st.session_state.Woman_e, on_change=check_woman_five
            )
        elif st.session_state.upper_long:
            write_category_avatar()
            Woman_a = st.checkbox(
                "여 1", value=st.session_state.Woman_a, on_change=check_woman_one
            )
            Woman_b = st.checkbox(
                "여 2", value=st.session_state.Woman_b, on_change=check_woman_two
            )
            Woman_c = st.checkbox(
                "여 3", value=st.session_state.Woman_c, on_change=check_woman_three
            )
            Woman_d = st.checkbox(
                "여 4", value=st.session_state.Woman_d, on_change=check_woman_four
            )
            Woman_e = st.checkbox(
                "여 5", value=st.session_state.Woman_e, on_change=check_woman_five
            )
            Man_a = st.checkbox(
                "남 1", value=st.session_state.Man_a, on_change=check_man_one
            )
            Man_b = st.checkbox(
                "남 2", value=st.session_state.Man_b, on_change=check_man_two
            )
            Man_c = st.checkbox(
                "남 3", value=st.session_state.Man_c, on_change=check_man_three
            )
            Man_d = st.checkbox(
                "남 4", value=st.session_state.Man_d, on_change=check_man_four
            )
            Man_e = st.checkbox(
                "남 5", value=st.session_state.Man_e, on_change=check_man_five
            )
        elif st.session_state.upper_short:
            write_category_avatar()
            Woman_a = st.checkbox(
                "여 1", value=st.session_state.Woman_a, on_change=check_woman_one
            )
            Woman_b = st.checkbox(
                "여 2", value=st.session_state.Woman_b, on_change=check_woman_two
            )
            Woman_c = st.checkbox(
                "여 3", value=st.session_state.Woman_c, on_change=check_woman_three
            )
            Woman_d = st.checkbox(
                "여 4", value=st.session_state.Woman_d, on_change=check_woman_four
            )
            Woman_e = st.checkbox(
                "여 5", value=st.session_state.Woman_e, on_change=check_woman_five
            )
            Man_a = st.checkbox(
                "남 1", value=st.session_state.Man_a, on_change=check_man_one
            )
            Man_b = st.checkbox(
                "남 2", value=st.session_state.Man_b, on_change=check_man_two
            )
            Man_c = st.checkbox(
                "남 3", value=st.session_state.Man_c, on_change=check_man_three
            )
            Man_d = st.checkbox(
                "남 4", value=st.session_state.Man_d, on_change=check_man_four
            )
            Man_e = st.checkbox(
                "남 5", value=st.session_state.Man_e, on_change=check_man_five
            )
        elif st.session_state.upper_etc:
            write_category_avatar()
            Woman_a = st.checkbox(
                "여 1", value=st.session_state.Woman_a, on_change=check_woman_one
            )
            Woman_b = st.checkbox(
                "여 2", value=st.session_state.Woman_b, on_change=check_woman_two
            )
            Woman_c = st.checkbox(
                "여 3", value=st.session_state.Woman_c, on_change=check_woman_three
            )
            Woman_d = st.checkbox(
                "여 4", value=st.session_state.Woman_d, on_change=check_woman_four
            )
            Woman_e = st.checkbox(
                "여 5", value=st.session_state.Woman_e, on_change=check_woman_five
            )
        elif st.session_state.lower_pantslong:
            write_category_avatar()
            Woman_a = st.checkbox(
                "여 1", value=st.session_state.Woman_a, on_change=check_woman_one
            )
            Woman_b = st.checkbox(
                "여 2", value=st.session_state.Woman_b, on_change=check_woman_two
            )
            Woman_c = st.checkbox(
                "여 3", value=st.session_state.Woman_c, on_change=check_woman_three
            )
            Woman_d = st.checkbox(
                "여 4", value=st.session_state.Woman_d, on_change=check_woman_four
            )
            Woman_e = st.checkbox(
                "여 5", value=st.session_state.Woman_e, on_change=check_woman_five
            )
            Man_a = st.checkbox(
                "남 1", value=st.session_state.Man_a, on_change=check_man_one
            )
            Man_b = st.checkbox(
                "남 2", value=st.session_state.Man_b, on_change=check_man_two
            )
            Man_c = st.checkbox(
                "남 3", value=st.session_state.Man_c, on_change=check_man_three
            )
            Man_d = st.checkbox(
                "남 4", value=st.session_state.Man_d, on_change=check_man_four
            )
            Man_e = st.checkbox(
                "남 5", value=st.session_state.Man_e, on_change=check_man_five
            )
        elif st.session_state.lower_pantsshort:
            write_category_avatar()
            Woman_a = st.checkbox(
                "여 1", value=st.session_state.Woman_a, on_change=check_woman_one
            )
            Woman_b = st.checkbox(
                "여 2", value=st.session_state.Woman_b, on_change=check_woman_two
            )
            Woman_c = st.checkbox(
                "여 3", value=st.session_state.Woman_c, on_change=check_woman_three
            )
            Woman_d = st.checkbox(
                "여 4", value=st.session_state.Woman_d, on_change=check_woman_four
            )
            Woman_e = st.checkbox(
                "여 5", value=st.session_state.Woman_e, on_change=check_woman_five
            )
            Man_a = st.checkbox(
                "남 1", value=st.session_state.Man_a, on_change=check_man_one
            )
            Man_b = st.checkbox(
                "남 2", value=st.session_state.Man_b, on_change=check_man_two
            )
            Man_c = st.checkbox(
                "남 3", value=st.session_state.Man_c, on_change=check_man_three
            )
            Man_d = st.checkbox(
                "남 4", value=st.session_state.Man_d, on_change=check_man_four
            )
            Man_e = st.checkbox(
                "남 5", value=st.session_state.Man_e, on_change=check_man_five
            )
        elif st.session_state.lower_skirtlong:
            write_category_avatar()
            Woman_a = st.checkbox(
                "여 1", value=st.session_state.Woman_a, on_change=check_woman_one
            )
            Woman_b = st.checkbox(
                "여 2", value=st.session_state.Woman_b, on_change=check_woman_two
            )
            Woman_c = st.checkbox(
                "여 3", value=st.session_state.Woman_c, on_change=check_woman_three
            )
            Woman_d = st.checkbox(
                "여 4", value=st.session_state.Woman_d, on_change=check_woman_four
            )
            Woman_e = st.checkbox(
                "여 5", value=st.session_state.Woman_e, on_change=check_woman_five
            )
        elif st.session_state.lower_skirtshort:
            write_category_avatar()
            Woman_a = st.checkbox(
                "여 1", value=st.session_state.Woman_a, on_change=check_woman_one
            )
            Woman_b = st.checkbox(
                "여 2", value=st.session_state.Woman_b, on_change=check_woman_two
            )
            Woman_c = st.checkbox(
                "여 3", value=st.session_state.Woman_c, on_change=check_woman_three
            )
            Woman_d = st.checkbox(
                "여 4", value=st.session_state.Woman_d, on_change=check_woman_four
            )
            Woman_e = st.checkbox(
                "여 5", value=st.session_state.Woman_e, on_change=check_woman_five
            )

        image_path = list()
        for key in sorted(st.session_state):
            if st.session_state[key]:
                image_path.append(key)

    # st.write(image_path)
    st.write("")

    # cloth file upload
    st.write("##### 👕  옷 사진을 업로드 해주세요.")

    files = list()

    uploaded_only_cloth_file = st.file_uploader(
        "Upload your cloth.",
        type=["jpg", "jpeg", "png"],
        key="z_only_cloth",
        label_visibility="hidden",
    )

    _, col, _ = st.columns([1, 3, 1])
    with col:
        if uploaded_only_cloth_file:
            cloth_image_bytes = uploaded_only_cloth_file.getvalue()
            cloth_image = Image.open(io.BytesIO(cloth_image_bytes)).resize((384, 512))

            cloth_image_byte_arr = io.BytesIO()
            cloth_image.save(cloth_image_byte_arr, format="PNG")
            cloth_image_bytes = cloth_image_byte_arr.getvalue()

            files.append(
                (
                    "cloth",
                    (
                        uploaded_only_cloth_file.name,
                        cloth_image_bytes,
                        uploaded_only_cloth_file.type,
                    ),
                )
            )

    col1, col2 = st.columns(2)
    with col1:
        if uploaded_only_cloth_file:
            st.image(cloth_image)
        # else:
        #    st.image(Image.open(os.path.join(dir_root, 'service/front-end/images/DALLE_illust_1.png')).resize((384, 512)))

    with col2:
        if len(image_path) >= 3:
            try:
                avatar_image_path = os.path.join(
                    dir_root,
                    f"service/back-end/sample_images/{image_path[1]}/{image_path[2].split('_')[1]}/{image_path[0]}.jpg",
                )
                avatar_image = Image.open(avatar_image_path)
                st.image(avatar_image.resize((384, 512)))
                files.append(("avatar_path", (avatar_image_path)))
            except IndexError:
                pass

    _, col, _ = st.columns([2, 0.71, 2])
    with col:
        inference = st.button("입어보기!")

    if inference and uploaded_only_cloth_file:
        _, col, _ = st.columns([2, 1, 2])
        with col:
            with st.spinner("입는 중 …"):
                response = requests.post(
                    "http://localhost:8501/cloth-tryon", files=files
                )

        result_image = Image.open(io.BytesIO(response.content))
        _, col, _ = st.columns([1, 2, 1])
        with col:
            st.image(result_image)

    elif inference:
        st.info("옷 사진을 업로드 해주세요.", icon="🔥")

    _, col2, _ = st.columns([2, 0.67, 2])
    with col2:
        if inference:
            try:
                btn = st.download_button(
                    label="다운로드",
                    data=response.content,
                    file_name="result.jpg",
                    mime="image/jpg",
                )
            except:
                pass


if __name__ == "__main__":
    main()
