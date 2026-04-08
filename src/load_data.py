import pandas as pd
import os

def load_car_data(filepath="data/cars_cleaned_dataset.csv"):
    """
    Loads the cleaned car dataset.
    Added error handling just in case the file is missing.
    """
    if not os.path.exists(filepath):
        print(f"CRITICAL ERROR: Data file not found at: {filepath}")
        print("Make sure 'cars_cleaned_dataset.csv' is inside the 'data/' folder.")
        return pd.DataFrame() 

    try:
        df = pd.read_csv(filepath)
        print("Data loaded successfully.")
        return df
    except Exception as e:
        print(f"Error while reading CSV: {e}")
        return pd.DataFrame()
