from pathlib import Path
import pandas as pd

blog_folder: Path = Path(__file__).parent
data_path: Path = blog_folder / 'data'


def load_db() -> pd.DataFrame:
    db_path = data_path / 'article_db.csv'
    if db_path.exists():
        return pd.read_csv(blog_folder / 'data' / 'article_db.csv',parse_dates=['date'])
    else:
        return pd.DataFrame(columns=['date','website_name','author','title','url'])