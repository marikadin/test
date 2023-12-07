import streamlit as st

def main():
    st.title("Streamlit Web Browser")

    # Button to open the website
    if st.button("Open Yahoo"):
        # Display the website in an iframe
        st.components.v1.html('<iframe src="https://www.yahoo.com/" width="1000" height="600"></iframe>', height=600)

if __name__ == "__main__":
    main()
