import pandas as pd
import os

csv_filename1 = "data/Climate_Data_2012_2022/3546991.csv"
csv_filename2 = "data/Climate_Data_2012_2022/3546990.csv"

df1 = pd.read_csv(csv_filename1)
df2 = pd.read_csv(csv_filename2)

combined_df = pd.concat([ df2,df1], ignore_index=True)

threshold = 15000
filtered_df = combined_df.dropna(axis=1, thresh=len(combined_df) - threshold)

combined_df.dropna(axis=1, thresh=len(combined_df) - threshold, inplace=True)
combined_df.drop(columns=['STATION','REPORT_TYPE','SOURCE','REPORT_TYPE.1','SOURCE.1',
                          'REM','HourlyStationPressure'],inplace=True)

df=combined_df

df['DATE'] = pd.to_datetime(df['DATE'])
df['DATE'] = df['DATE'].dt.round('H')

numeric_columns = ["HourlyAltimeterSetting", "HourlyDewPointTemperature", "HourlyWindSpeed",
                   "HourlyRelativeHumidity", "HourlyVisibility", "HourlyWetBulbTemperature"]
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

df = df.set_index('DATE').ffill().bfill().reset_index()
result = df.groupby(['DATE']).agg({**{col: 'mean' for col in numeric_columns}}).reset_index()

csv_filename = 'data/Climate_Data_2012_2022/3546991_3546990_cleaned.csv'
result.to_csv(csv_filename, index=False)