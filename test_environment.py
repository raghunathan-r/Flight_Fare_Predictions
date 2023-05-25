import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Load the data frame to get the options for user
dataset = pd.read_csv('data\processed\cleaned_dataset_2023.csv')
user_inputs = dict()

st.header("Flight Fare Prediction App")

Date_of_journey = st.date_input("Date of Journey", label_visibility="visible")
print("Date of Journey: ", Date_of_journey)

user_inputs["Journey_date"] = int(Date_of_journey.day)
print(Date_of_journey.day)
user_inputs["Journey_month"] = int(Date_of_journey.month)
print(Date_of_journey.month)

print("user_inputs[Journey_date]: ", user_inputs["Journey_date"])
print("user_inputs[Journey_month]: ", user_inputs["Journey_month"])
print(user_inputs)

# JOURNEY DATE AND MONTH AND DAY

day_options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_chosen = st.selectbox("Day", day_options)
user_inputs["Journey_day_encoded"] = day_options.index(day_chosen) + 1
print(user_inputs["Journey_day_encoded"])
print(user_inputs)

# CLASS

class_options = list(dataset['Class'].unique())
class_chosen = st.selectbox('Flight Class', class_options)
user_inputs['Class'] = class_options.index(class_chosen)

# AIRLINE

airline_options = dataset["Airline"].unique()
airline_chosen = st.selectbox('Airline', dataset['Airline'].unique())

for airline in airline_options:
    if airline == airline_chosen:
        user_inputs[airline] = 1
    else:
        user_inputs[airline] = 0

# SOURCE

source_options = dataset["Source"].unique()
source_chosen = st.selectbox('Source', dataset['Source'].unique())

for source in source_options:
    if source == source_chosen:
        user_inputs["Source_" + source] = 1
    else:
        user_inputs["Source_" + source] = 0

# DESTINATION

destination_options = dataset["Destination"].unique()
destination_chosen = st.selectbox("Destination", dataset["Destination"].unique())

for destination in destination_options:
    if destination == destination_chosen:
        user_inputs["Destination_" + destination] = 1
    else:
        user_inputs["Destination_" + destination] = 0

# DEPARTURE

departure_options = dataset["Departure"].unique()
print("\nDeparture options: ", departure_options)
departure_options = sorted(departure_options, key=lambda x: ('Before' in x, 'AM' in x, 'Noon' in x, 'After' in x))
print("\nDeparture options: ", departure_options)

departure_chosen = st.selectbox("Departure", dataset["Departure"].unique())
user_inputs["Departure_encoded"] = departure_options.index(departure_chosen) + 1

# ARRIVAL

arrival_options = dataset["Arrival"].unique()
arrival_options = sorted(arrival_options, key=lambda x: ('Before' in x, 'AM' in x, 'Noon' in x, 'After' in x))

arrival_chosen = st.selectbox("Arrival", dataset["Arrival"].unique())
user_inputs["Arrival_encoded"] = arrival_options.index(arrival_chosen) + 1

# TOTAL STOPS

total_stops = st.selectbox('Total Stops', dataset['Total_stops'].unique())
user_inputs['Total_stops'] = ['non-stop', '1-stop', '2+-stop'].index(total_stops)

user_inputs["Days_left"] = st.number_input('Days Left for Journey', min_value=0, max_value=365, value=30)

# Duration_in_hours

user_inputs["Duration_in_hours"] = st.number_input('Duration of Flight in Hours', min_value=0.0, max_value=24.0, value=2.5)

user_inputs_df = pd.DataFrame.from_dict([user_inputs])
user_inputs_df = user_inputs_df.sort_index(axis=1)
print("WITHOUT .head()\n", user_inputs_df)
# user_inputs_df = user_inputs_df.drop(["Air India", "Destination_Ahmedabad", "Source_Ahmedabad"], axis = 1, inplace = True)

# user_inputs_df.to_csv('./../data/interim/user_inputs.csv', index=False)
# print(user_inputs_df.type())


if st.button("Predict Price"):
    # print(user_inputs.head())
    # user_inputs = pd.read_csv('./../data/interim/user_inputs.csv')
    print(user_inputs_df)

    # Print the data frame
    # user_inputs = user_inputs.sort_index(axis=1)
    # st.write(user_inputs.head())

    model = pickle.load(open("models\\voting_regressor.pkl", "rb"))

    user_inputs_df = user_inputs_df.drop(["Air India", "Destination_Ahmedabad", "Source_Ahmedabad"], axis=1)

    predicted_price = model.predict(user_inputs_df)
    print(predicted_price)
    st.write("Predicted price = " + str(predicted_price))