import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Load the data frame to get the options for user
df = pd.read_csv('data\processed\cleaned_dataset_2023.csv')
user_inputs = pd.DataFrame()

st.header("Flight Fare Prediction App")

user_inputs["Journey_date"] = st.date_input('Journey Date')


# ---------------

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
duration = st.number_input('Duration of Flight in Hours', min_value=0.0, max_value=24.0, value=2.5)

# airline = st.selectbox('Airline', df.columns[df.columns.str.startswith('Airline_')])
airline_cols = df.columns[df.columns.str.startswith('Airline_')]
airline_options = [col.replace('Airline_', '') for col in airline_cols]
airline = "Airline_" + st.selectbox('Airline', airline_options)

class_cols = df.columns[df.columns.str.startswith('Class_')]
class_options = [col.replace('Class_', '') for col in class_cols]
flight_class = "Class_" + st.selectbox('Flight Class', class_options)

source = st.selectbox('Source', df.columns[df.columns.str.startswith('Source_')])

departure = st.selectbox('Departure', df.columns[df.columns.str.startswith('Departure_')])

total_stops = st.selectbox('Total Stops', df.columns[df.columns.str.startswith('Total_stops_')])

arrival = st.selectbox('Arrival', df.columns[df.columns.str.startswith('Arrival_')])

destination = st.selectbox('Destination', df.columns[df.columns.str.startswith('Destination_')])

# # Create a new row for the user inputs
# user_inputs = pd.DataFrame({
#     'Journey_date': [journey_date],
#     'Journey_day': [journey_day],
#     'Days_left': [days_left],
#     'Duration_in_hours': [duration],
#     **{col: [0] for col in df.columns if col not in [journey_day, airline, flight_class, source, departure, total_stops, arrival, destination]}
# })
# Create a new row for the user inputs
user_inputs = pd.DataFrame({
    'Journey_date': [journey_date],
    'Journey_day': [journey_day],
    'Days_left': [days_left],
    'Duration_in_hours': [duration],
    **{col: [0] for col in df.columns if col not in cat_features}
})
user_inputs.drop(["Date_of_journey", "Journey_day"], axis=1, inplace=True)

user_inputs[airline] = 1
user_inputs[flight_class] = 1
user_inputs[source] = 1
user_inputs[departure] = 1
user_inputs[total_stops] = 1
user_inputs[arrival] = 1
user_inputs[destination] = 1


if st.button("Predict Price"):
    print(df.columns)

    # Print the dataframe
    user_inputs = user_inputs.sort_index(axis=1)
    st.write(user_inputs)

    model = pickle.load(open("models\\voting_regressor.pkl", "rb"))

    predicted_price = model.predict(user_inputs)
    st.write("Flight Fare = " + predicted_price)
