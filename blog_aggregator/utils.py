from typing import Union
from pathlib import Path
import pandas as pd

blog_folder: Path = Path(__file__).parent

data_path: Path = blog_folder / 'data'
db_path: Path = data_path / 'article_db.csv'

BLOG_FIELDS = ['date','website_name','author','title','url']


class MissingDbException(Exception):
    pass


def create_db(columns=BLOG_FIELDS, db_path: Union[str,Path]=db_path):
    """Create a pandas df with the specified columns, and save it as a csv in the desired location."""
    df_db = pd.DataFrame(columns=BLOG_FIELDS)
    df_db.to_csv(db_path,index=False)
    
    return df_db

def load_db(db_path: Union[str,Path]=db_path) -> pd.DataFrame:
    """Loads in the database"""
    if db_path.exists():
        return pd.read_csv(db_path, parse_dates=['date'])
    else:
        raise MissingDbException(f'Sorry, no database found at location {db_path=}')

