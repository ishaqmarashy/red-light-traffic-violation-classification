import pandas as pd
import os
from datetime import datetime, timedelta

csv_filename = 'data/Climate_Data_2012_2022/asos.csv'

df = pd.read_csv(csv_filename)
df['valid'] = pd.to_datetime(df['valid'], format='%Y-%m-%d %H:%M')

threshold = 10000
filtered_df = df.dropna(axis=1, thresh=len(df) - threshold)

df.dropna(axis=1, thresh=len(df) - threshold, inplace=True)
df.drop(columns=['metar','station'],inplace=True)

numeric_columns = ['tmpf','dwpf','sknt',  'relh', 'alti','vsby', 'feel']
df['date_hour'] = df['valid'].dt.round('H')
result = df.groupby(['date_hour']).agg({**{col: 'mean' for col in numeric_columns}, 'skyc1': 'first'}).reset_index()

start_date = datetime(2012, 1, 1)
end_date = datetime(2020, 12, 31, 23) 
expected_dates = pd.date_range(start=start_date, end=end_date, freq='H')
reference_df = pd.DataFrame({'date_hour': expected_dates})

merged_df = pd.merge(reference_df, result, on='date_hour', how='outer')

filled_df = merged_df.set_index('date_hour').ffill().bfill().reset_index()

csv_filename = 'data/Climate_Data_2012_2022/asos_clean.csv'
filled_df.to_csv(csv_filename, index=False)
