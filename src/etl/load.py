import os
import pandas as pd

def load(data_frame: pd.DataFrame, file_name: str) -> str:
    """
    Recebe um dataframe e salva como .csv

    Parameters
    ----------
    data_frame (pd.DataFrame): dataframe a ser salvo como excel
    file_name (str): nome do arquivo a ser salvo

    return: "Arquivo salvo com sucesso"

    """
    output_path = os.path.dirname(__file__) + '\\output'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    data_frame.to_csv(f"{output_path}/{file_name}.csv", index=False, sep=';')
    return "Arquivo salvo com sucesso"