from kalshi_tools import *
import pandas as pd

data = pd.read_csv('data/kalshi_filtered.csv')


data['resolution_criteria'] = data['rules_primary'].fillna('') + ' ' + data['rules_secondary'].fillna('')
data['resolution_criteria'] = data['resolution_criteria'].str.strip()


example = get_edsl_table("ARCTICICEMIN-24OCT01-T4.2", data)  # 🔄 swap for a real ticker
def add_to_master_db(example):
  master_db_path = 'data/kalshi_master.parquet'
  try:
    master_db = pd.read_parquet(master_db_path)
  except FileNotFoundError:
    master_db = pd.DataFrame()

  master_db = pd.concat(
    [master_db, example],
    axis=0,           # 0 = rows  (axis=1 would append columns)
    ignore_index=True
  )

  master_db.drop_duplicates(inplace=True)
  master_db.to_parquet(master_db_path)

example.columns
add_to_master_db(example)
example.to_parquet('test.parquet')


