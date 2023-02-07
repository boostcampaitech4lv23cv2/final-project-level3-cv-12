import io
import os
from pathlib import Path

import requests
from PIL import Image

import streamlit as st


# SETTING PAGE CONFIG TO WIDE MODE
ASSETS_DIR_PATH = os.path.join(Path(__file__).parent.parent.parent.parent, "assets")

st.set_page_config(
    page_title="Virtual Try-On",
    # layout="wide",
    # page_icon=":bird:",
    # initial_sidebar_state="expanded"
)

def main():
    dir_root = os.getcwd()
    st.write()
    st.image(Image.open(os.path.join(dir_root, 'service/front-end/images/main_illust.png')))
    
    for _ in range(5):
        st.write("")
    _, col, _ = st.columns([1, 6, 1])
    with col:
        st.title("의류 가상 피팅 서비스 :blue[ViTA]")
    _, col, _ = st.columns([1, 1.22, 1])
    with col:
        st.write("## :blue[Vi]rtual :blue[T]ry-on :blue[A]ll")
    for _ in range(7):
        st.write("")

    col1, col2 = st.columns([1.5,2])
    with col1:
        for _ in range(5):
            st.write("")
        st.write("##### 온라인 쇼핑몰에서도\n ##### :blue[입어보고] 구매하세요.")
        st.write("")
        st.write("의류 가상 피팅 서비스로")
        st.write("나에게 어울리는 옷을")
        st.write("손쉽게 찾을 수 있습니다.")
        for _ in range(3):
            st.write("")
    with col2:
        st.image(Image.open(os.path.join(dir_root, 'service/front-end/images/intro_1.png')))

        
    for _ in range(5):
        st.write("")

        
    col1, col2 = st.columns([2,1.5])
    with col1:
        st.image(Image.open(os.path.join(dir_root, 'service/front-end/images/intro_2.png')))
    with col2:
        for _ in range(5):
            st.write("")
        st.write("##### 소비자에게 :orange[부담없이]\n ##### 착용 사진을 제공하세요.")
        st.write("")
        st.write("기존 착용 사진에 다른 옷을 입혀")
        st.write("다양한 착용 사진을 효율적으로")
        st.write("만들 수 있습니다.")
        for _ in range(3):
            st.write("")
            

    for _ in range(8):
        st.write("")

    
    st.write("### 👕 사용자 지정 모델 활용하기")
    st.write("##### :blue[원하는 모델 사진을 업로드해서 옷을 입힙니다.]")
    _, col, _ = st.columns([1, 5, 1])
    with col:
        st.image(Image.open(os.path.join(dir_root, 'service/front-end/images/manual_custom.png')))
    st.write(
        """
        ① 입을 옷 유형을 선택합니다. \n
        ② 옷 사진을 업로드합니다. \n
        ③ 모델 사진을 업로드합니다. \n
        ④ "입어보기" 버튼을 클릭하면 잠시 후 결과가 나타납니다. \n
        ⑤ "저장하기" 버튼으로 사진을 다운로드 받을 수 있습니다. \n
        """
    )

    for _ in range(5):
        st.write("")
    
    st.write("### 제공된 모델 활용하기")
    st.write("##### :blue[제공된 모델 사진에 옷을 입힙니다.]")
    _, col, _ = st.columns([1, 5, 1])
    with col:
        st.image(Image.open(os.path.join(dir_root, 'service/front-end/images/manual_provided.png')))
    st.write(
        """
        ① 입을 옷 유형을 선택합니다. \n
        ② 옷을 입힐 모델 사진을 선택합니다. \n
        ③ 옷 사진을 업로드합니다. \n
        ④ "입어보기" 버튼을 클릭하면 잠시 후 결과가 나타납니다. \n
        ⑤ "저장하기" 버튼으로 사진을 다운로드 받을 수 있습니다. \n
        """
    )

    for _ in range(5):
        st.write("")

if __name__ == '__main__':
    main()