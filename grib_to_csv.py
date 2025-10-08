
import xarray as xr

ds = xr.open_dataset("./site_weather_data/sshf2.grib", engine="cfgrib")
print(ds)


# Define your bounding box

lat_min, lat_max = 53.2, 53.4
lon_min, lon_max = -7.70, -7.5

# Subset the data over the spatial rectangle
subset = ds.sel(
    latitude=slice(lat_max, lat_min),  # Decreasing order in many datasets
    longitude=slice(lon_min, lon_max)  # Increasing order
) 



# Compute the spatial mean for 't' and 'z' over lat/lon, preserving time and pressure
v10 = subset['v10'].mean(dim=['latitude', 'longitude'])
u10 = subset['u10'].mean(dim=['latitude', 'longitude'])
#t2m = ds['t2m'].mean(dim=['latitude', 'longitude'])
#tcc = ds['tcc'].mean(dim=['latitude', 'longitude'])
blh = subset['blh'].mean(dim=['latitude', 'longitude'])
sshf = subset['sshf'].mean(dim=['latitude', 'longitude'])

v10 = v10.to_dataframe(name='v10').reset_index()
u10 = u10.to_dataframe(name='u10').reset_index()
#t2m = t2m.to_dataframe(name='t2m').reset_index()
#tcc = tcc.to_dataframe(name='tcc').reset_index()
blh = blh.to_dataframe(name='blh').reset_index()
sshf = sshf.to_dataframe(name='sshf').reset_index()
sshf['sshf'] = sshf['sshf']/3600 # Convert from J/m² to W/m² assuming 1-hour accumulation
v10['u10'] = u10['u10']
v10['blh'] = blh['blh']

v10.to_csv('comp_data.csv', index=False)
sshf.to_csv('sshf_data.csv', index=False)
# Optionally, combine into a new dataset
result = xr.Dataset({'t_mean': t_mean, 'z_mean': z_mean})
