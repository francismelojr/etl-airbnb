import os
from etl.extract import extract 
from etl.transform import transform
from etl.load import load

if __name__ == '__main__':
    extract('Florianópolis - Santa Catarina')
    df = transform(os.path.dirname(__file__) + '\\etl\\output')
    load(df, 'final')