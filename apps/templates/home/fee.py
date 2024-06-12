import json
import pandas as pd
import numpy as np

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import matplotlib.pyplot as plt

# Function to read JSON file
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

path1="C:\\Users\\HP\\Downloads\\fee_master.json"
path2="C:\\Users\\HP\\Downloads\\receipt_master.json"

data1=read_json_file(path1)
data2=read_json_file(path2)
df1=pd.DataFrame(data1)
df2=pd.DataFrame(data2)

# Merge the DataFrames on 'fee_id'
df = pd.merge(df1, df2, on='fee_id', how='outer')

# Drop columns that won't be used in the prediction
df = df.drop(columns=['receipt_id_x', 'receipt_id_y', 'fee_id'])

# Convert dates to datetime
df['due_date'] = pd.to_datetime(df['due_date'])
df['receipt_date'] = pd.to_datetime(df['receipt_date'])

# Extract date features
df['due_year'] = df['due_date'].dt.year
df['due_month'] = df['due_date'].dt.month
df['receipt_year'] = df['receipt_date'].dt.year
df['receipt_month'] = df['receipt_date'].dt.month

# Drop original date columns
df = df.drop(columns=['due_date', 'receipt_date'])

# Fill missing values (if any) with 0
df = df.fillna(0)

# Define the feature set and the target variable
X = df.drop(columns=['fee_amt'])
y = df['fee_amt']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Print predictions for the test set
predictions = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
print(predictions)
