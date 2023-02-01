import streamlit as st

def check_dress():
    st.session_state.dress, st.session_state.upper, st.session_state.lower = 1, 0, 0
    st.session_state.dress_long, st.session_state.dress_short, st.session_state.dress_etc = 0, 0, 0
    st.session_state.upper_long, st.session_state.upper_short, st.session_state.upper_etc = 0, 0, 0
    st.session_state.lower_pantslong, st.session_state.lower_pantsshort, st.session_state.lower_skirtlong, st.session_state.lower_skirtshort = 0, 0, 0, 0
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 0, 0
def check_upper():
    st.session_state.dress, st.session_state.upper, st.session_state.lower = 0, 1, 0
    st.session_state.dress_long, st.session_state.dress_short, st.session_state.dress_etc = 0, 0, 0
    st.session_state.upper_long, st.session_state.upper_short, st.session_state.upper_etc = 0, 0, 0
    st.session_state.lower_pantslong, st.session_state.lower_pantsshort, st.session_state.lower_skirtlong, st.session_state.lower_skirtshort = 0, 0, 0, 0
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 0, 0
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 0, 0, 0
def check_lower():
    st.session_state.dress, st.session_state.upper, st.session_state.lower = 0, 0, 1
    st.session_state.dress_long, st.session_state.dress_short, st.session_state.dress_etc = 0, 0, 0
    st.session_state.upper_long, st.session_state.upper_short, st.session_state.upper_etc = 0, 0, 0
    st.session_state.lower_pantslong, st.session_state.lower_pantsshort, st.session_state.lower_skirtlong, st.session_state.lower_skirtshort = 0, 0, 0, 0
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 0, 0
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 0, 0, 0

def check_dress_long():
    st.session_state.dress_long, st.session_state.dress_short, st.session_state.dress_etc = 1, 0, 0
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 0, 0
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 0, 0, 0
def check_dress_short():
    st.session_state.dress_long, st.session_state.dress_short, st.session_state.dress_etc = 0, 1, 0
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 0, 0
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 0, 0, 0
def check_dress_etc():
    st.session_state.dress_long, st.session_state.dress_short, st.session_state.dress_etc = 0, 0, 1
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 0, 0
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 0, 0, 0

def check_upper_long():
    st.session_state.upper_long, st.session_state.upper_short, st.session_state.upper_etc = 1, 0, 0
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 0, 0
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 0, 0, 0
def check_upper_short():
    st.session_state.upper_long, st.session_state.upper_short, st.session_state.upper_etc = 0, 1, 0
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 0, 0
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 0, 0, 0
def check_upper_etc():
    st.session_state.upper_long, st.session_state.upper_short, st.session_state.upper_etc = 0, 0, 1
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 0, 0
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 0, 0, 0

def check_lower_pants_long():
    st.session_state.lower_pantslong, st.session_state.lower_pantsshort, st.session_state.lower_skirtlong, st.session_state.lower_skirtshort = 1, 0, 0, 0
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 0, 0
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 0, 0, 0
def check_lower_pants_short():
    st.session_state.lower_pantslong, st.session_state.lower_pantsshort, st.session_state.lower_skirtlong, st.session_state.lower_skirtshort = 0, 1, 0, 0
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 0, 0
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 0, 0, 0
def check_lower_skirt_long():
    st.session_state.lower_pantslong, st.session_state.lower_pantsshort, st.session_state.lower_skirtlong, st.session_state.lower_skirtshort = 0, 0, 1, 0
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 0, 0
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 0, 0, 0
def check_lower_skirt_short():
    st.session_state.lower_pantslong, st.session_state.lower_pantsshort, st.session_state.lower_skirtlong, st.session_state.lower_skirtshort = 0, 0, 0, 1
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 0, 0
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 0, 0, 0

def check_woman_one():
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 1, 0, 0, 0, 0
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 0, 0, 0
def check_woman_two():
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 1, 0, 0, 0
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 0, 0, 0
def check_woman_three():
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 1, 0, 0
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 0, 0, 0
def check_woman_four():
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 1, 0
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 0, 0, 0
def check_woman_five():
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 0, 1
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 0, 0, 0

def check_man_one():
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 1, 0, 0, 0, 0
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 0, 0
def check_man_two():
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 1, 0, 0, 0
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 0, 0
def check_man_three():
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 1, 0, 0
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 0, 0
def check_man_four():
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 0, 1, 0
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 0, 0
def check_man_five():
    st.session_state.Man_a, st.session_state.Man_b, st.session_state.Man_c, st.session_state.Man_d, st.session_state.Man_e = 0, 0, 0, 0, 1
    st.session_state.Woman_a, st.session_state.Woman_b, st.session_state.Woman_c, st.session_state.Woman_d, st.session_state.Woman_e = 0, 0, 0, 0, 0