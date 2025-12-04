import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


df = pd.read_csv("Dallas_Police_Incidents_cleaned.csv", low_memory=False)
print(df.head())

print(df['zip_code'].unique()[:10]) #Preview some values
print(df['zip_code'].isnull())      #Check for missing Zip Codes


df['zip_code'] = pd.to_numeric(df['zip_code'], errors='coerce')
df = df.dropna(subset=['zip_code'])


#Count Incidents per Zip codes
zip_counts = df['zip_code'].value_counts().sort_index()
print(zip_counts.head(10))

#Making it into a DataFrame
zip_summary = zip_counts.reset_index()
zip_summary.columns = ['zip_code', 'incident_count']
#print(zip_summary.head()) 


# #Bar Chart of Top Zips
top_zip = zip_summary.nlargest(10, 'incident_count')

plt.figure(figsize=(10,6))
plt.bar(top_zip['zip_code'].astype(str), top_zip['incident_count'])
plt.title("Top 10 ZIP Codes by Number of Incidents in Dallas")
plt.xlabel("ZIP Code")
plt.ylabel("Number of Incidents")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# #Exploring Zip Codes over time
df['date1'] = pd.to_datetime(df['date1'], errors='coerce')
df['Year'] = df['date1'].dt.year

df = df[df['Year'] >= 2013]

zip_trend = (
    df.groupby(['zip_code', 'Year'])
    .size()
    .reset_index(name='incident_count')
    .sort_values(['zip_code', 'Year'])
)

zip_list = [75217, 75211, 75227]  # add any you want
subset = zip_trend[zip_trend['zip_code'].isin(zip_list)]

for z in zip_list:
    data = subset[subset['zip_code'] == z]
    plt.plot(data['Year'], data['incident_count'], label=z)

plt.title("Incident Trends by ZIP Code (2013–Present)")
plt.xlabel("Year")
plt.ylabel("Number of Incidents")
plt.legend(title="ZIP Code")
plt.grid(True)
plt.show()

#focusing on zip code 75217
zip_75217 = zip_trend[zip_trend['zip_code'] == 75217]

plt.figure(figsize=(8, 5))
plt.plot(zip_75217['Year'], zip_75217['incident_count'], marker='o')
plt.title("Crime Incidents Over Time (ZIP 75217)")
plt.xlabel("Year")
plt.ylabel("Number of Incidents")
plt.grid(True)
plt.show()

#Incedents Geographically
# Example: assuming the geometry column is named "geocoded_column"
df[['lon', 'lat']] = df['geocoded_column'].str.extract(r'POINT \(([-\d\.]+) ([-\d\.]+)\)').astype(float)


#Drops missing values
df = df.dropna(subset=['lon', 'lat'])

#Ploting with Plotly
fig = px.scatter_map(
    df.sample(1000, random_state=42),  # sample for performance
    lat="lat",
    lon="lon",
    hover_name="zip_code",
    hover_data=["nibrs_crime_category"],
    color_discrete_sequence=["red"],
    zoom=9,
    height=600
)

fig.update_layout(
    map_style="open-street-map",
    title="Dallas Police Incidents by Location"
)

fig.show()

#Checkig Coordinates 
print(df[['geocoded_column', 'lon', 'lat']].head())
