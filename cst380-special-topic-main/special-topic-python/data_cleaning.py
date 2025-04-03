# @Author: Logan Powser
## @Date: 3/18/2025
## @Abstract: Data cleaning for model that is to be trained and handed to an iOS app

### imports
import pandas as pd
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#read file
path = Path('./dataset/vehicles.csv')
df = pd.read_csv(path, parse_dates=['posting_date'], infer_datetime_format=True)

df = df[df['price']  >  0]

df.dropna(subset=['transmission'], inplace=True)

def convert_condition(df, column='condition'):
    """
    Converts condition values in the dataframe using a predefined mapping.

    Parameters:
    df (pandas.DataFrame): The dataframe containing the condition column
    column (str): Name of the column to convert, defaults to 'condition'

    Returns:
    pandas.DataFrame: Dataframe with converted condition values
    """
    # Create the condition mapping dictionary
    condition_mapping = {
        'salvage': 0,
        'fair': 1,
        'good': 2,
        'excellent': 3,
        'new': 4,
        'like new': 4
    }

    # Create a copy of the dataframe to avoid modifying the original
    df_copy = df.copy()

    # Apply the mapping to the specified column
    df_copy[column] = df_copy[column].map(condition_mapping)

    # Check if any values weren't mapped (will be NaN after mapping)
    unmapped = df_copy[column].isna() & df[column].notna()
    if unmapped.any():
        print(f"Warning: {unmapped.sum()} values in '{column}' column couldn't be mapped.")
        print("Unique unmapped values:", df.loc[unmapped, column].unique())

    return df_copy

df_processed = df.copy()

df_processed['posting_date'] = pd.to_datetime(df_processed['posting_date'], format='%Y-%m-%d %H:%M:%S%z', errors='coerce')
reference_date = df['posting_date'].max()
df_processed['car_age'] = (reference_date.year - df_processed['year'])

df_processed = convert_condition(df_processed)

df_processed.drop(['posting_date', 'manufacturer', 'cylinders', 'title_status', 'state', 'VIN', 'id', 'paint_color', 'fuel', 'drive', 'type', 'transmission'], axis=1, inplace=True)

df_processed.info()

def corr_map(df: pd.DataFrame, name:str)->None:
    plt.figure(figsize=(12,10))
    plt.title(f'Correlation Map for {name} Data')
    sns.heatmap(df.corr(), annot=True, cmap='inferno')
    plt.xticks(rotation=45)
    plt.show()

#corr_map(df_processed.corr(), "Used Car")

df_processed.to_csv('./dataset/vehicles_processed0.csv', index=False)

#td list
# cylinders: wrap 5, 10, 3, and 12 cylinder values into other? if still not significant, delete and use integer values
# type
# other vars