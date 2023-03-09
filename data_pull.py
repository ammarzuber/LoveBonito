import requests
import pandas as pd
from datetime import datetime
from geopy.geocoders import Nominatim
import json
from sqlalchemy import create_engine
import uuid


host="localhost"
user="root"
password="root"
database = "singapore_taxi"
port = 3306





def get_connection():
    engine =  create_engine("mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database), echo=False)
    return engine


def reverse_geocode(row):
  geolocator = Nominatim(user_agent="geoapiExercises")
  location = geolocator.reverse(str(row['Latitude']) + ", " + str(row['Longitude']))
  return location.raw['address']






engine = get_connection()



# Extract data from API endpoint
response = requests.get("https://api.data.gov.sg/v1/transport/taxi-availability")
data = response.json()["features"][0]["geometry"]["coordinates"]

# Convert data to DataFrame

df = pd.DataFrame(data)
df = df.rename(columns={0: "Longitude", 1: "Latitude"})



df['geom'] = df.apply(lambda row: (str(row.Latitude),str(row.Longitude)),axis=1)
df['geom'] = df['geom'].astype(str)


print (df)


# df["address"] = list(map(lambda el: locator.reverse(el).raw['address'], df["geom"]))

df['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
df['unique_id'] =  df.apply(lambda _: uuid.uuid4(), axis=1)

df['metadata'] = df.apply(reverse_geocode, axis=1)

df['unique_id'] = df['unique_id'].astype(str)
json_struct = json.loads(df.to_json(orient="records"))
df = pd.json_normalize(json_struct)

cities_taxis = df['metadata.suburb'].value_counts().rename_axis('city').reset_index(name='taxi_available')





df.to_sql(name='taxi_location_current', con=engine, if_exists = 'replace' )
df.to_sql(name='taxi_location_history', con=engine, if_exists = 'append' )
cities_taxis.to_sql(name='cities_taxi', con=engine , if_exists = 'replace')









