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
    st.title("Virtual Try-On Test")

    st.info("Welcome !!!", icon="💡")

    st.header("Inroduction this project")

    st.write("virtual try-on service")

    st.write("Go to the first page if you want to dress up our avatars")

    st.write("Go to the second page if you want to dress up your body")

if __name__ == '__main__':
    main()