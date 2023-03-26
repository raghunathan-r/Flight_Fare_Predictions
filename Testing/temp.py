import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import VotingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load data
data = pd.read_excel('train_dataset_kaggle.xlsx')

# Preprocess data
data['Journey_day'] = pd.to_datetime(data['Date_of_Journey'], format='%d/%m/%Y').dt.day
data['Journey_month'] = pd.to_datetime(data['Date_of_Journey'], format='%d/%m/%Y').dt.month
data.drop(['Date_of_Journey'], axis=1, inplace=True)

data['Dep_hour'] = pd.to_datetime(data['Dep_Time']).dt.hour
data['Dep_min'] = pd.to_datetime(data['Dep_Time']).dt.minute
data.drop(['Dep_Time'], axis=1, inplace=True)

data['Arrival_hour'] = pd.to_datetime(data['Arrival_Time']).dt.hour
data['Arrival_min'] = pd.to_datetime(data['Arrival_Time']).dt.minute
data.drop(['Arrival_Time'], axis=1, inplace=True)


# Calculating the Duration. It is the diffrence between departure and arrival time. Then extracting the duration hours and minutes from it

duration = list(data["Duration"])

for i in range(len(duration)):
    # checking if it conatins only hours or mins
    if len(duration[i].split()) != 2:
        if "h" in duration[i]:
            duration[i] = duration[i].strip() + " 0m"
        else:
            duration[i] = "0h " + duration[i]

duration_hours = []
duration_mins = []

# Extracting only hours and mins from duration
for i in range(len(duration)):
    duration_hours.append(int(duration[i].split(sep = "h")[0]))
    duration_mins.append(int(duration[i].split(sep = "m")[0].split()[-1]))

# Adding Duration Hours and minues extracted to the data frame
data["Duration_hours"] = duration_hours
data["Duration_mins"] = duration_mins

# Dropping the Duration that is extracted
data.drop(["Duration"], axis = 1, inplace = True)

data['Airline'].replace({
    'Jet Airways': 'Jet Airways',
    'IndiGo': 'IndiGo',
    'Air India': 'Air India',
    'Multiple carriers': 'Multiple carriers',
    'SpiceJet': 'SpiceJet',
    'Vistara': 'Vistara',
    'Air Asia': 'Air Asia',
    'GoAir': 'GoAir',
    'Multiple carriers Premium economy': 'Multiple carriers Premium economy',
    'Jet Airways Business': 'Jet Airways Business',
    'Vistara Premium economy': 'Vistara Premium economy',
    'Trujet': 'Trujet'
}, inplace=True)

airline = pd.get_dummies(data['Airline'], drop_first=True)

source = pd.get_dummies(data['Source'], drop_first=True)

destination = pd.get_dummies(data['Destination'], drop_first=True)

data.drop(['Route', 'Additional_Info'], axis=1, inplace=True)

data = pd.concat([data, airline, source, destination], axis=1)

data.drop(["Airline", "Source", "Destination"], axis = 1, inplace = True)
           
# Encode categorical variables
cat_cols = ['Source', 'Destination', 'Route', 'Additional_Info']
for col in cat_cols:
    encoder = LabelEncoder()
    data[col] = encoder.fit_transform(data[col])

# Splitting data into training and testing sets
train_data = data.loc[data['Source_Train'] == 1]
test_data = data.loc[data['Source_Test'] == 1]
train_data.drop(['Source_Train', 'Source_Test'], axis=1, inplace=True)
test_data.drop(['Source_Train', 'Source_Test'], axis=1, inplace=True)

# Splitting the data into features and target variable
X_train = train_data.drop('Price', axis=1)
y_train = train_data['Price']
X_test = test_data.drop('Price', axis=1)
y_test = test_data['Price']

# Creating the models
models = [('rf', RandomForestRegressor(n_estimators=100, random_state=42)),
          ('gb', GradientBoostingRegressor(random_state=42)),
          ('xgb', XGBRegressor(random_state=42))]

# Creating the voting regressor
voting_regressor = VotingRegressor(estimators=models, n_jobs=-1)

# Fitting the model
voting_regressor.fit(X_train, y_train)

# Predicting the values
y_pred = voting_regressor.predict(X_test)

# Calculating the mean absolute error
mae = mean_absolute_error(y_test, y_pred)
print("Mean Absolute Error:", mae)

