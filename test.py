import streamlit as st
import subprocess

keyword = st.text_input("Enter keyword")
if st.button("Submit"):
    st.write("You entered:", keyword)
    import main