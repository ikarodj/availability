import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Load data
hotel_data = pd.DataFrame(columns=['Check In Date', 'Hotel Name', 'Port', 'Rooms Available', 'Price', 'Breakfast', 'Breakfast Price', 'Dinner', 'Dinner Price'])
check_in_date = datetime.date(2024, 7, 26)  # Default check-in date

# Sidebar options
st.sidebar.title("Options")
selected_port = st.sidebar.radio("Select Port", ['ORY', 'CDG'])

# Form for data input
st.header("Hotel Availability Management")
with st.form("hotel_input_form"):
    check_in_date = st.date_input("Check In Date", check_in_date)
    hotel_name = st.selectbox("Hotel Name", ['Hotel A', 'Hotel B', 'Hotel C'], 
                              help="Select the hotel name from the dropdown list.")
    rooms_available = st.number_input("Rooms Available", min_value=0, 
                                      help="Enter the number of rooms available.")
    price = st.number_input("Price", min_value=0.0, 
                            help="Enter the price per room.")
    
    st.subheader("Meals")
    has_breakfast = st.checkbox("Can Serve Breakfast?")
    if has_breakfast:
        breakfast_included = st.radio("Breakfast Included?", ("Yes", "No"))
        if breakfast_included == "No":
            breakfast_price = st.number_input("Breakfast Price", min_value=0.0, 
                                              help="Enter the price for breakfast.")
        else:
            breakfast_price = 0.0
    else:
        breakfast_price = None

    has_dinner = st.checkbox("Can Serve Dinner?")
    if has_dinner:
        dinner_price = st.number_input("Dinner Price", min_value=0.0, 
                                       help="Enter the price for dinner.")
    else:
        dinner_price = None

    submit_button = st.form_submit_button("Add to Availability")

# Add new entry to data
if submit_button:
    new_entry = pd.DataFrame({
        'Check In Date': [check_in_date],
        'Hotel Name': [hotel_name],
        'Port': [selected_port],
        'Rooms Available': [rooms_available],
        'Price': [price],
        'Breakfast': [has_breakfast],
        'Breakfast Price': [breakfast_price],
        'Dinner': [has_dinner],
        'Dinner Price': [dinner_price]
    })
    hotel_data = pd.concat([hotel_data, new_entry], ignore_index=True)

# Display data table
st.subheader("Hotel Availability Overview")
if not hotel_data.empty:
    filtered_data = hotel_data[(hotel_data['Port'] == selected_port) & 
                               (hotel_data['Check In Date'] >= check_in_date)]
    st.dataframe(filtered_data.reset_index(drop=True))
    # Line chart to visualize trends in availability over time
    st.subheader("Availability Trends Over Time")
    availability_chart_data = filtered_data.groupby('Check In Date')['Rooms Available'].sum().reset_index()
    st.bar_chart(availability_chart_data.set_index('Check In Date'))
else:
    st.info("No data available.")

# Download button for data
st.subheader("Download Data")
csv_data = hotel_data.to_csv(index=False)
st.download_button(label="Download CSV", data=csv_data, file_name="hotel_availability.csv", mime="text/csv")

# User feedback
if submit_button:
    st.success("Data successfully added to availability.")
