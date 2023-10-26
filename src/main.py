import os

from etl.extract import extract
from etl.load import load
from etl.transform import transform

if __name__ == '__main__':
    extract('Florianópolis - Santa Catarina')
    df = transform(os.path.dirname(__file__) + '\\etl\\output')
    load(df, 'final')
