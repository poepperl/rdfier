from pathlib import Path
from unco import UNCO_PATH
import streamlit as st

st.set_page_config(
    page_title="Input Format",
    layout="wide")

# st.title('Input Format')

st.markdown(Path(UNCO_PATH,"docu/1_input_format.md").read_text(), unsafe_allow_html=True)