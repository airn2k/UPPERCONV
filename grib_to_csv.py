
import xarray as xr

ds = xr.open_dataset("upper.grib", engine="cfgrib")
print(ds)

#Print data units
print(ds['t'].attrs['units'])

# Define your bounding box
# 52.47N  8.16W 

lat_min, lat_max = 52.4, 52.6
lon_min, lon_max = -8.2, -8.0

# Subset the data over the spatial rectangle
subset = ds.sel(
    latitude=slice(lat_max, lat_min),  # Decreasing order in many datasets
    longitude=slice(lon_min, lon_max)  # Increasing order
) 



# Compute the spatial mean for 't' and 'z' over lat/lon, preserving time and pressure
v = subset['v'].mean(dim=['latitude', 'longitude'])
u = subset['u'].mean(dim=['latitude', 'longitude'])
r = subset['r'].mean(dim=['latitude', 'longitude'])
z = subset['z'].mean(dim=['latitude', 'longitude'])
t = subset['t'].mean(dim=['latitude', 'longitude'])

v = v.to_dataframe(name='v').reset_index()
u = u.to_dataframe(name='u').reset_index()
r = r.to_dataframe(name='r').reset_index()
z = z.to_dataframe(name='z').reset_index()
t = t.to_dataframe(name='t').reset_index()

# Convert geopotential height to meters
z['z'] = z['z'] / 9.81
# calculate wind speed in tenths of m/s
s = ((v['v']**2 + u['u']**2)**0.5)*10
# calculate wind direction in degrees
d = (180/3.14159) * (3.14159 + (3.14159/2) - (3.14159/2) * ((u['u']/s) / abs(u['u']/s)) * (3.14159/2 - (3.14159/4) * ((u['u']/s)**2) / ((u['u']/s)**2 + (v['v']/s)**2)))
d = d % 360 
# calculate dew point temperature in tenths of degree celcsius, t is in K, r is relative humidity in %
td = (t['t'] - 273.15) - ((100 - r['r']) / 5)
td = td * 10

# create a new data frame with all the variables
df = v[['time', 'isobaricInhPa']].copy()
df['height'] = z['z']
df['dew_point'] = td
df['temperature'] = (t['t'] - 273.15) * 10  # Convert K to tenths of °C
df['wind_direction'] = d
df['wind_speed'] = s

# Save to CSV
df.to_csv("upper_air_data.csv", index=False)
