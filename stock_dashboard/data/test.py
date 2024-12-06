import pandas as pd
from pathlib import Path

script_dir = Path(__file__).parent/"assets/all_sectors.csv"
print('Path:', script_dir)
df = pd.read_csv(script_dir)
print(df.shape)
print(df.head(2))
print(df['Sector'].unique())
print(df[df['Sector']=='Error'].shape)
print(df[df['Industry']=='Error'].shape)