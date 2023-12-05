import streamlit as st
import datetime

def main():
    st.title("Choose start date")

    # Set the minimum and maximum selectable dates
    min_date = datetime.date(2022, 1, 1)
    max_date = datetime.date.today()

    # Get user input for a date within the specified range, with a default value
    selected_date = st.date_input("Select a date", min_value=min_date, max_value=max_date, value=min_date)

    # Add a text input for stock name
    stock_name = st.text_input("Enter Stock Name")

    # Add a button to save the stock name
    if st.button("Save Stock Name"):
        if not stock_name:
            st.warning("You must enter a stock name!")
        else:
            st.success(f"Stock Name '{stock_name}' saved!")

    # Display the selected date
    st.write("You selected:", selected_date)

if __name__ == "__main__":
    main()
