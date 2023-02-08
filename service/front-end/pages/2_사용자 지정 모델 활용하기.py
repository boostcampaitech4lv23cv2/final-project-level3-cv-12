import io
import os
from pathlib import Path

import requests
from PIL import Image

import streamlit as st
import numpy as np

# SETTING PAGE CONFIG TO WIDE MODE
ASSETS_DIR_PATH = os.path.join(Path(__file__).parent.parent.parent.parent, "assets")


def check_dress():
    st.session_state.dress, st.session_state.upper, st.session_state.lower = 1, 0, 0


def check_upper():
    st.session_state.dress, st.session_state.upper, st.session_state.lower = 0, 1, 0


def check_lower():
    st.session_state.dress, st.session_state.upper, st.session_state.lower = 0, 0, 1


# initial
if "dress" not in st.session_state:
    st.session_state.dress = 0
    st.session_state.upper = 0
    st.session_state.lower = 0


def main():
    cloth_category = ["드레스", "상의", "하의"]
    cloth_states = [
        st.session_state.dress,
        st.session_state.upper,
        st.session_state.lower,
    ]
    cloth_on_changes = [check_dress, check_upper, check_lower]
    dir_root = os.getcwd()

    guide_line_path = os.path.join(dir_root, "service/front-end/images/guide_line.png")
    guide_image = Image.open(guide_line_path).convert("RGB").resize((768, 1024))

    _, col, _ = st.columns([1, 3.2, 1])
    with col:
        st.title("의류 가상 피팅 서비스")
    _, col, _ = st.columns([1, 1.8, 1])
    with col:
        st.write("### 사용자 지정 모델 활용하기")
    for _ in range(3):
        st.write("")

    # guide
    guide = st.checkbox("권장 사항", key="zz_guide_2")
    if guide:
        st.info(
            """
            옷은 겹쳐서 가려지는 부분이 없는 사진을 업로드 해주세요. \n

            모델이 가이드선에 맞게 위치한 정면 사진을 업로드 해주세요. (아래 그림 참고) \n

            모델을 업로드하면 가이드선이 그려진 사진이 보여집니다. (결과에는 나오지않습니다.) \n

            모델이 입을 옷과 유사한 형태의 옷을 입은 사진을 권장합니다.
            """
        )
        _, col, _ = st.columns([1, 2, 1])
        with col:
            st.image(
                Image.open(
                    os.path.join(
                        dir_root, "service/front-end/images/guide_image_1.1.png"
                    )
                ).resize((384, 512))
            )

    st.write("##### ✔ 입을 옷 유형을 선택해 주세요.")
    st.write("")

    cols = st.columns(3)
    for idx, col in enumerate(cols):
        with col:
            st.checkbox(
                cloth_category[idx],
                value=cloth_states[idx],
                on_change=cloth_on_changes[idx],
            )

    files = list()
    if st.session_state.dress:
        files.append(("part", ("dress")))
    if st.session_state.upper:
        files.append(("part", ("upper")))
    if st.session_state.lower:
        files.append(("part", ("lower")))

    for _ in range(3):
        st.write("")

    col1, col2 = st.columns(2)
    with col1:
        st.write("##### 👕  옷 사진을 업로드 해주세요.")
        uploaded_cloth_file = st.file_uploader(
            "Upload your cloth.",
            type=["jpg", "jpeg", "png"],
            key="cloth",
            label_visibility="hidden",
        )

        if uploaded_cloth_file:
            cloth_image_bytes = uploaded_cloth_file.getvalue()
            cloth_image = Image.open(io.BytesIO(cloth_image_bytes)).resize((768, 1024))

            cloth_image_byte_arr = io.BytesIO()
            cloth_image.save(cloth_image_byte_arr, format="PNG")
            cloth_image_bytes = cloth_image_byte_arr.getvalue()

            st.image(cloth_image.resize((384, 512)))

            files.append(
                (
                    "cloth",
                    (
                        uploaded_cloth_file.name,
                        cloth_image_bytes,
                        uploaded_cloth_file.type,
                    ),
                )
            )
        # else:
        #    st.image(Image.open(os.path.join(dir_root, 'service/front-end/images/DALLE_illust_1.png')).resize((384, 512)))

    with col2:
        st.write("##### 🧍‍♀️  모델 사진을 업로드 해주세요.")
        uploaded_human_file = st.file_uploader(
            "Upload your avatar.",
            type=["jpg", "jpeg", "png"],
            key="body",
            label_visibility="hidden",
        )

        if uploaded_human_file:
            human_image_bytes = uploaded_human_file.getvalue()
            human_image = Image.open(io.BytesIO(human_image_bytes)).resize((768, 1024))

            combine_image = Image.blend(human_image, guide_image, 0.4)

            human_image_byte_arr = io.BytesIO()
            human_image.save(human_image_byte_arr, format="PNG")
            human_image_bytes = human_image_byte_arr.getvalue()

            st.image(combine_image.resize((384, 512)))
            files.append(
                (
                    "human",
                    (
                        uploaded_human_file.name,
                        human_image_bytes,
                        uploaded_human_file.type,
                    ),
                )
            )
        else:
            st.image(
                Image.open(
                    os.path.join(
                        dir_root, "service/front-end/images/guide_image_1.1.png"
                    )
                ).resize((384, 512))
            )

    for _ in range(2):
        st.write("")

    _, col, _ = st.columns([2, 0.71, 2])
    with col:
        inference = st.button("입어보기!")

    if inference:
        if uploaded_cloth_file and uploaded_human_file:
            _, col2, _ = st.columns([2, 1, 2])
            with col2:
                with st.spinner("입는 중 …"):
                    response = requests.post(
                        "http://localhost:8501/all-tryon", files=files
                    )

            result_image = Image.open(io.BytesIO(response.content))
            _, col, _ = st.columns([1, 2, 1])
            with col:
                st.image(result_image.resize((384, 512)))
        else:
            st.info("사진을 업로드 해주세요.", icon="🔥")

    _, col2, _ = st.columns([2, 0.67, 2])
    with col2:
        if inference:
            btn = st.download_button(
                label="다운로드",
                data=response.content,
                file_name="result.jpg",
                mime="image/jpg",
            )


if __name__ == "__main__":
    main()
