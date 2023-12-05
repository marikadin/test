import streamlit as st
import datetime

def main():
    st.title("Streamlit Calendar Example")

    # Get user input for a date using date_input
    selected_date = st.date_input("Select a date", datetime.date.today())

    # Display the selected date
    st.write("You selected:", selected_date)

if __name__ == "__main__":
    main()