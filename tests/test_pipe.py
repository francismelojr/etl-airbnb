def test_transform():
    import os

    import pandas as pd

    from src.etl.transform import transform

    current_directory = os.path.dirname(os.path.realpath(__file__))
    output_dir = os.path.abspath(os.path.join(current_directory, os.pardir, "src", "etl", "output"))

    data1 = {
    'col1': ['A', 'B', 'C', 'D'],
    'col2': [10, 20, 30, 40]
    }
    df1 = pd.DataFrame(data1)

    data2 = {
        'Nome': ['E', 'F', 'G', 'H'],
        'Idade': [50, 60, 70, 80]
    }
    df2 = pd.DataFrame(data2)

    path_df1 = os.path.join(output_dir, 'df1.csv')
    path_df2 = os.path.join(output_dir, 'df2.csv')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df1.to_csv(path_df1, sep=';')
    df2.to_csv(path_df2, sep=';')

    df = transform(output_dir)

    os.remove(path_df1)
    os.remove(path_df2)

    assert isinstance(df, pd.DataFrame)
