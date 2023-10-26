def test_extract():
    import pandas as pd

    from src.etl.extract import extract

    df = extract('Rio de Janeiro', headless=True)
    assert isinstance(df, pd.DataFrame)


def test_transform():
    import os

    import pandas as pd

    from src.etl.transform import transform

    current_path = os.getcwd()
    relative_path = '\src\etl\output'
    final_path = current_path + relative_path

    df = transform(path=final_path)

    assert isinstance(df, pd.DataFrame)
