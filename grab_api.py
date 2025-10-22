import requests
import pandas as pd
import numpy as np
import matplotlib
import json


def grab_data(url, date, name, per_page=100):
    """gets a Json file from the given URL


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




def to_dataframe(data_path):
    observations = None
    with open(data_path, "r") as f:
        raw_data = json.load(f)
        observations = raw_data[1]
    data = pd.DataFrame(observations)
    data = data.drop(columns=["indicator", "country", "unit", "obs_status", "decimal"])
    print(data.head())
    return data


def chart_data(data):
    #TODO plots
    return None

