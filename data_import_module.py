# path/filename: backtesting_framework/data_importer.py

import pandas as pd
import numpy as np
from datetime import datetime
import re
import requests
from sqlalchemy import create_engine

class DataImporter:
    def __init__(self):
        pass

    def read_csv(self, file_path):
        """
        Reads data from a CSV file and returns a pandas DataFrame.
        """
        try:
            data = pd.read_csv(file_path)
            self.validate_data(data)
            return data
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return None

    def read_database(self, db_connection_string, query):
        """
        Reads data from a database using a SQL query and returns a pandas DataFrame.
        """
        try:
            engine = create_engine(db_connection_string)
            data = pd.read_sql(query, engine)
            self.validate_data(data)
            return data
        except Exception as e:
            print(f"Error reading from database: {e}")
            return None

    def read_api(self, api_url, params=None):
        """
        Reads data from an API endpoint and returns a pandas DataFrame.
        """
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            data = pd.DataFrame(response.json())
            self.validate_data(data)
            return data
        except Exception as e:
            print(f"Error reading from API: {e}")
            return None

    def validate_data(self, data):
        """
        Enhances the data validation process.
        """
        # Check for required columns
        required_columns = {'Date': str, 'Open': float, 'High': float, 'Low': float, 'Close': float, 'Volume': int}
        for column, expected_type in required_columns.items():
            if column not in data.columns:
                raise ValueError(f"Missing required column: {column}")
            if not all(isinstance(val, expected_type) for val in data[column].dropna()):
                raise TypeError(f"Incorrect type for column: {column}")

        # Validate date format (assuming format: YYYY-MM-DD)
        date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
        if not all(re.match(date_pattern, str(date)) for date in data['Date']):
            raise ValueError("Date column contains invalid dates")

        # Handling missing values
        if data.isnull().values.any():
            # Placeholder for handling missing values, e.g., imputation or exclusion
            pass
        
        # Handle missing values based on user configuration
        if self.handle_missing == 'delete':
            data.dropna(inplace=True)
        elif self.handle_missing == 'impute':
            # Placeholder for imputation logic, e.g., mean, median imputation
            pass
        elif self.handle_missing == 'default':
            data.fillna(0, inplace=True)  # or any other default value

        # Handle missing values based on user configuration
        if self.handle_missing == 'delete':
            data.dropna(inplace=True)
        elif self.handle_missing == 'interpolate':
            data.interpolate(method='linear', inplace=True)
        elif self.handle_missing == 'default':
            data.fillna(0, inplace=True)  # or any other default value

        return data