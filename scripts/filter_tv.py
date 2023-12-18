import pandas as pd
import os

csv_filename = "data/Traffic_Violations/Traffic_Violations.csv"
df = pd.read_csv(csv_filename)

df.dropna(subset=['Description'], inplace=True)
Red_df = df[df['Description'].str.contains('red', case=False) & df['Description'].str.contains('stop', case=False)]
Red_Accident=Red_df[Red_df['Accident'].str.contains('Yes', case=False)]
Red_Accident_2=Red_Accident
Red_Accident_2['DV']= ((Red_Accident_2['Fatal']=='Yes') | (Red_Accident_2['Personal Injury']=='Yes')).astype(int)
Red_Accident_2.to_csv('data/Traffic_Violations/Traffic_violations_Reduced.csv', index=False)
