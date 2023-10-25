#libraries
import pandas as pd
import os

def transform(path):
    """"
    Function to transform all files extracted to a single dataframe.
    
    Parameters
    ----------
    path : str
        Path of csv files to read and transform.
    
    """

    files = [file for file in os.listdir(path) if file.endswith(".csv")]

    frames = []

    for file in files:
        path_file = os.path.join(path, file)
        data = pd.read_csv(path_file, sep=";")
        frames.append(data)

    df = pd.concat(frames, ignore_index=True)
    return df