def test_transform():
    import os

    import pandas as pd

    from src.etl.transform import transform

    current_directory = os.path.dirname(os.path.realpath(__file__))
    output_dir = os.path.abspath(os.path.join(current_directory, os.pardir, "src", "etl", "output"))

    df = transform(path=output_dir)

    assert isinstance(df, pd.DataFrame)
