import streamlit as st
import datetime

def main():
    st.title("Streamlit Calendar Example with Default Date")

    # Set the minimum and maximum selectable dates
    min_date = datetime.date(2022, 1, 1)
    max_date = datetime.date.today()

    # Get user input for a date within the specified range, with a default value
    selected_date = st.date_input("Select a date", min_value=min_date, max_value=max_date, value=min_date)

    # Display the selected date
    st.write("You selected:", selected_date)

if __name__ == "__main__":
    main()
