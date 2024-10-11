import pandas as pd
import numpy as np

# Load the dataset with the correct delimiter (comma in this case)
data = pd.read_csv('data/dataset.txt', delimiter=',')

# Check the columns for leading/trailing whitespaces and clean them
data.columns = data.columns.str.strip()

# Display the column names to ensure they are correct
print("Columns after stripping whitespaces: ", data.columns)

# Check for missing columns
print("\nData Head (First few rows):")
print(data.head())

# Part 1: Identify inconsistencies
# ---------------------------------

# 1. Handle missing data
# ----------------------
# Check for missing values in the dataset
print("\nMissing Data Check (Before):")
print(data.isnull().sum())

# Fill missing 'Age' with the median age (assuming it is a numeric column)
if 'Age' in data.columns:
    data['Age'] = pd.to_numeric(data['Age'], errors='coerce')  # Ensure Age is numeric
    data['Age'] = data['Age'].fillna(data['Age'].median())
else:
    print("'Age' column not found.")

# Fill missing 'Price' with the mean price
if 'Price' in data.columns:
    data['Price'] = pd.to_numeric(data['Price'], errors='coerce')  # Ensure Price is numeric
    data['Price'] = data['Price'].fillna(data['Price'].mean())
else:
    print("'Price' column not found.")

# For text fields like 'custName', 'Product', 'AdvertisingAgency', fill missing values with 'Unknown'
if 'custName' in data.columns:
    data['custName'] = data['custName'].fillna('Unknown')

if 'AdvertisingAgency' in data.columns:
    data['AdvertisingAgency'] = data['AdvertisingAgency'].fillna('Unknown')

# 2. Fix inconsistent formats
# ----------------------------
# Standardize the 'DatePurchased' column to the format YYYY-MM-DD
if 'DatePurchased' in data.columns:
    data['DatePurchased'] = pd.to_datetime(data['DatePurchased'], errors='coerce')

# Ensure 'RatingOfProduct' is numeric, and handle any non-numeric values
if 'RatingOfProduct' in data.columns:
    data['RatingOfProduct'] = pd.to_numeric(data['RatingOfProduct'], errors='coerce')

# 3. Handle outliers
# ------------------
# Identify outliers in 'Age' and 'Price' columns and replace them (as previously discussed)

# For 'Age' column
if 'Age' in data.columns:
    Q1_age = data['Age'].quantile(0.25)
    Q3_age = data['Age'].quantile(0.75)
    IQR_age = Q3_age - Q1_age
    lower_bound_age = Q1_age - 1.5 * IQR_age
    upper_bound_age = Q3_age + 1.5 * IQR_age
    median_age = data['Age'].median()
    data['Age'] = np.where((data['Age'] < lower_bound_age) | (data['Age'] > upper_bound_age), median_age, data['Age'])

# For 'Price' column
if 'Price' in data.columns:
    Q1_price = data['Price'].quantile(0.25)
    Q3_price = data['Price'].quantile(0.75)
    IQR_price = Q3_price - Q1_price
    lower_bound_price = Q1_price - 1.5 * IQR_price
    upper_bound_price = Q3_price + 1.5 * IQR_price
    mean_price = data['Price'].mean()
    data['Price'] = np.where((data['Price'] < lower_bound_price) | (data['Price'] > upper_bound_price), mean_price, data['Price'])

# 4. Correct typographical errors
# -------------------------------
# For 'AdvertisingAgency', strip spaces and standardize text format
if 'AdvertisingAgency' in data.columns:
    data['AdvertisingAgency'] = data['AdvertisingAgency'].str.strip().str.title()

# 5. Handle duplicates
# --------------------
# Remove duplicates if any
if 'custID' in data.columns:
    data.drop_duplicates(subset=['custID'], inplace=True)

# Part 2: Re-check for inconsistencies and print cleaned data
print("\nMissing Data Check (After):")
print(data.isnull().sum())

# Save the cleaned data to Excel format
data.to_excel('Cleaned_Customer_Data.xlsx', index=False, engine='openpyxl')

print("\nData cleaning complete! File saved as 'Cleaned_Customer_Data.xlsx'.")
