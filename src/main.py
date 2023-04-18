import streamlit as st
import pandas as pd

# Load the dataframe
df = pd.read_csv('flight_data.csv')

# Convert the categorical features into arrays
cat_features = ['Airline', 'Class', 'Source', 'Departure', 'Total_stops', 'Arrival', 'Destination']
for feature in cat_features:
    dummies = pd.get_dummies(df[feature], prefix=feature)
    df = pd.concat([df, dummies], axis=1)
    df.drop(feature, axis=1, inplace=True)

# Get the user inputs
journey_date = st.date_input('Journey Date')
journey_day = st.selectbox('Journey Day', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
days_left = st.number_input('Days Left for Journey', min_value=0, max_value=365, value=30)
duration = st.number_input('Duration of Flight in Hours', min_value=0, max_value=24, value=2.5)
fare = st.number_input('Fare', min_value=0, max_value=100000, value=5000)

airline = st.selectbox('Airline', df.columns[df.columns.str.startswith('Airline_')])
flight_code = st.text_input('Flight Code', value='AI-101')
flight_class = st.selectbox('Flight Class', df.columns[df.columns.str.startswith('Class_')])
source = st.selectbox('Source', df.columns[df.columns.str.startswith('Source_')])
departure = st.selectbox('Departure', df.columns[df.columns.str.startswith('Departure_')])
total_stops = st.selectbox('Total Stops', df.columns[df.columns.str.startswith('Total_stops_')])
arrival = st.selectbox('Arrival', df.columns[df.columns.str.startswith('Arrival_')])
destination = st.selectbox('Destination', df.columns[df.columns.str.startswith('Destination_')])

# Create a new row for the user inputs
user_inputs = pd.DataFrame({
    'Journey_date': [journey_date],
    'Journey_day': [journey_day],
    'Days_left': [days_left],
    'Duration_in_hours': [duration],
    'Fare': [fare],
    airline: [1],
    'Flight_code': [flight_code],
    flight_class: [1],
    source: [1],
    departure: [1],
    total_stops: [1],
    arrival: [1],
    destination: [1]
})

# Append the new row to the dataframe
df = pd.concat([df, user_inputs], ignore_index=True)

# Print the dataframe
st.write(df)
