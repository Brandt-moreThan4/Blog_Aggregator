from pathlib import Path
import pandas as pd

blog_folder: Path = Path(__file__).parent


def load_db() -> pd.DataFrame:
    return pd.read_csv(blog_folder / 'data' / 'article_db.csv',parse_dates=['date'])