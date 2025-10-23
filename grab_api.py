import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
    for df in dataframes[1:]:
        merged = merged.merge(df, on=columns, how='outer')
    return merged


def chart_data(data, x, y, name):
    """Creates a scatterplot of two data columns, x, and y

    Args:
        data (dataframe): the dataframe that has the data
        x (str): x-column name for the data
        y (str): y-column name for the data
        name: what you want the chart to be called
    """
    plt.figure(figsize=(10, 6))
    
    plt.scatter(data[x], data[y], color='blue', s=100, alpha=0.6, edgecolors='black')

    plt.xlabel(x, fontsize=12)
    plt.ylabel(y, fontsize=12)
    
    mask = ~(data[x].isna() | data[y].isna())
    x_clean = data[x][mask]
    y_clean = data[y][mask]
    
    z = np.polyfit(x_clean, y_clean, 1)  
    p = np.poly1d(z)
    
    plt.plot(x_clean, p(x_clean), "r--", linewidth=2, label=f'y={z[0]:.2f}x+{z[1]:.2f}')
    plt.legend()
    plt.title(f'{y} vs {x}', fontsize=14, fontweight='bold')

    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    
    plt.savefig(name + '.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Graph saved as 'line_graph.png'")

def dataframe_to_json(data, filename):
    data.to_json(filename, orient='records', indent=4)
    