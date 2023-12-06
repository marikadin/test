import streamlit as st
import subprocess

keyword = st.text_input()
if st.button("Submit"):
    st.write("You entered:", keyword)
    import test