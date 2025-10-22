import requests
import pandas as pd
import numpy as np
import matplotlib as plt
import json


def grab_data(url, date, name, per_page=100):
    """gets a Json file from the given URL, preferably a world bank api url


    Args:
        url (str): a url to an api database
        date (str): the date (year) to grab data from
        name (str): name of the file the json file will be save to
        per_page (int): number of results per page. Defaults to 100


    Returns:
        str: filepath that the data was saved to
    """
    params = {
        'format': 'json',
        'date': date,
        'per_page': per_page
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        filename= name+ '.json'
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print("Data saved to " + filename)
    else:
        print("Failed to retrieve data:", response.status_code)

def clean_data(data):
    """drops all data with na values

    Args:
        data (dataframe): the dataframe to clean

    Returns:
        dataframe: the cleaned dataframe
    """
    data = data.dropna()
    return data


def to_dataframe(data_path):
    """converts a json file obtained by grab_data to a dataframe

    Args:
        data_path (str): the path to the json file

    Returns:
        dataframe: the dataframe representation of the json file
    """
    observations = None
    with open(data_path, "r") as f:
        raw_data = json.load(f)
        observations = raw_data[1]
    data = pd.DataFrame(observations)
    indicator_code = data['indicator'].iloc[0]['id']
    data = data.drop(columns=["indicator", "countryiso3code",  "unit", "obs_status", "decimal"])
    data['country'] = data['country'].apply(lambda x: x['value'])
    data.rename(columns={'value': indicator_code}, inplace=True)
    print(data.head())
    return data

def merge_datasets(dataframes, columns):
    """merges several dataframes on a list of given column

    Args:
        dataframes (list): a list of dataframes
        column (list): the columns of the dataframe to merge on
    """
    merged = dataframes[0].copy()
    for df in dataframes:
        merged = merged.merge(df, on=columns, how='outer')
    return merged


def chart_data(data):
    # plt.figure(figsize=(10, 6))
    # plt.plot(accuracies, 'bo-', linewidth=2, markersize=8)
    # plt.xlabel('Tree Depth')
    # plt.ylabel('Accuracy')
    # plt.title('Decision Tree Accuracy vs. Maximum Depth')
    # plt.grid(True, alpha=0.3)
    # plt.xticks(range(len(accuracies)))
    
    # plt.tight_layout()
    # plt.savefig('./decision_tree_accuracy.png', dpi=300, bbox_inches='tight')
    # plt.close() 
    return None

