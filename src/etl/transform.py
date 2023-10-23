#libraries
import pandas as pd
import os

def transform(path, export=False):
    """"
    Function to transform all files extracted to a single dataframe.
    
    Parameters
    ----------
    path : str
        Path of csv files to read and transform.

    export : str
        If True, the result will be exported to a csv file.
    """

    files = [file for file in os.listdir(path) if file.endswith(".csv")]

    frames = []

    for file in files:
        path_file = os.path.join(path, file)
        data = pd.read_csv(path_file, sep=";")
        frames.append(data)

    df = pd.concat(frames, ignore_index=True)

    if export == True:
        df.to_csv('final_data.csv', index=False, sep=";")
    
    return df