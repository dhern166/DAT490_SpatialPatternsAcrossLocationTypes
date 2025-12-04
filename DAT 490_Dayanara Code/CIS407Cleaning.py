
import pandas as pd
import numpy as np

df = pd.read_csv('Dallas_PoliceIncidents.csv', low_memory=False)

#Dataset Info
print("Before cleaning rows:")
print(df.shape)
print(df.head())
print(df.dtypes)


#Converting black strings to NaN
df.replace(' ', np.nan, inplace=True)

#Check for missing values
missing = df.isnull().sum()
#print(missing.sort_values(ascending=False).head(20))


#Removess and handles unsable columns
threshold = 0.8 * len(df)
cols_to_drop = [col for col in df.columns if df[col].isnull().sum() > threshold]
df.drop(columns=cols_to_drop, inplace=True)
#print("Dropped columns:", cols_to_drop)


#convert date/time columns
df['date1'] = pd.to_datetime(df['date1'], errors='coerce')
df['callreceived'] = pd.to_datetime(df['callreceived'], errors='coerce')


#clean numeric coulums
df['zip_code'] = pd.to_numeric(df['zip_code'], errors='coerce')

#Standerize categorical columns
df['offincident'] = df['offincident'].astype('category')


#rows with complete data for DateOccured, IncidentType, and Zip_Code
key_cols = ['date1', 'offincident', 'zip_code']
df.dropna(subset=key_cols, inplace=True)


#removes duplicates
dup_count = df.duplicated().sum()
#print(f"Duplicate rows: {dup_count}")
df.drop_duplicates(inplace=True)

print("\n")

#re-check
print("After cleaning rows:")
print(df.shape)
print(df.head())
print(df.dtypes)
#print("Missing after cleaning:", df.isnull().sum().head(10))

#Saving clean dataset
df.to_csv('Dallas_Police_Incidents_cleaned.csv', index=False)

