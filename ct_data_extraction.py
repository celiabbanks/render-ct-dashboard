# This is the working code for extracting clinical trial data pertaining to Pfizer.
# This code will test the lambda function before loading into AWS.

# data_extraction.py

import requests
import pandas as pd

def extract_data():
    csv_file_path = 'ct_data_pfizer.csv'  # Path to your CSV file
    df = pd.read_csv(csv_file_path)
    return df
