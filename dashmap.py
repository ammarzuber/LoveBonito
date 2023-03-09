
import geopandas as gpd
import pandas as pd
import mysql.connector


conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="singapore_taxi",
  port = 3306
)


# Retrieve data from database
query = """
SELECT Latitude, Longitude, timestamp, `metadata.suburb`,unique_id
FROM taxi_location_current

"""
df = pd.read_sql_query(query, conn)

# Create a new geopandas dataframe
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']))

# Set the coordinate reference system to EPSG 4326 (WGS84)
gdf.crs = 'EPSG:4326'
df['datetime'] = pd.to_datetime(df['timestamp'])

gdf['minute'] = gdf['datetime'].dt.minute







import plotly.express as px

city_counts = df.groupby('metadata.suburb')['unique_id'].count().reset_index()
top_city_counts = city_counts.sort_values(by='unique_id', ascending=False).head(10)
least_city_counts = city_counts.sort_values(by='unique_id', ascending=True).head(10)

# Create the bar graph
fig1 = px.bar(top_city_counts, x='metadata.suburb', y='unique_id', title='Top 10 Cities With Available Taxis')



fig3 = px.bar(least_city_counts, x='metadata.suburb', y='unique_id', title='Bottom 10 Cities With Available Taxis')

fig3.show()



# Create the scatter plot
fig2 = px.scatter_mapbox(gdf, lat='Latitude', lon='Longitude', zoom=10)


# Set the mapbox style
fig2.update_layout(mapbox_style='open-street-map')


fig2.show()

import plotly.subplots as sp

fig = sp.make_subplots(rows=1, cols=2, specs=[[{'type': 'bar'}, {'type': 'bar'}]],subplot_titles=('Top 10 Cities With Available Taxis','Bottom 10 Cities With Available Taxis'))

# Add the scatter plot to the figure
fig.add_trace(fig1['data'][0], row=1, col=1)

# Add the bar graph to the figure
fig.add_trace(fig3['data'][0], row=1, col=2)

# Show the plot
fig.show()




