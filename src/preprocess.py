import polars as pl
import geojson

# Clean the AQI data
# read the data
aqi_data = pl.read_csv("../data/AQI_data.csv")

# # filter to only lahore

aqi_data_lhe = aqi_data.filter(pl.col('city') == 'Lahore')

month_map = {
    '01':'January', 
    '02': 'February', 
    '03': 'March', 
    '04': 'April', 
    '05': 'May', 
    '06': 'June', 
    '07': 'July', 
    '08': 'August', 
    '09': 'September', 
    '10': 'October', 
    '11': 'November', 
    '12': 'December'
}


aqi_data_lhe_clean = aqi_data_lhe.with_columns(pl.col('timestamp')
                                         .str.split('-')
                                         .alias('date_split')).with_columns(
                                             pl.col("date_split").list.get(0).alias('year'), 
                                             pl.col('date_split').list.get(1).alias('month')
                                         ).with_columns(pl.col('month')
                                                        .replace(month_map)
                                                        .alias("full_month_name")
                                         ).drop('date_split').filter(pl.col("us_aqi").is_not_null())



aqi_mon_avg = aqi_data_lhe_clean.group_by(['station_name', 
                                           'latitude', 
                                           'longitude', 
                                           'year', 
                                           'full_month_name'
                                           ]).agg(
                                               pl.col('us_aqi').mean().alias('avg_aqi')
                                           ).sort('avg_aqi', descending = True)
print(aqi_mon_avg.head(10))

# convert data to a geojson
features = []

for row in aqi_mon_avg.iter_rows(named = True):
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row["longitude"], row["latitude"]]
        },
        "properties": {
            "avg_aqi": row["avg_aqi"],
            "year": row["year"], 
            "month": row["full_month_name"], 
            "station_name": row["station_name"]
        }
    }
    features.append(feature)

geojson_obj = geojson.FeatureCollection(features)
with open('../data/aqi_lhe_data.geojson', 'w') as f:
    geojson.dump(geojson_obj, f)




# # clean the sectoral emissions 
# pol_lst = ['PM2.5', 'SOx', 'NOx', 'CO']
# sectoral_emissions = pl.read_csv("../data/sectoral_data_lhe.csv")

# sectoral_emissions_fil = sectoral_emissions.filter(pl.col('pollutant').is_in(pol_lst))


# sector_aggregates = sectoral_emissions_fil.group_by('sector').agg(
#     pl.col('emissions').sum().alias('total_emissions')
# )

# #print(sector_aggregates.head(10))

# sector_pollutant_agg = \
# sectoral_emissions_fil.group_by(['sector', 'pollutant']).agg(
#     pl.col('emissions').sum().alias('total_emissions')

# ).sort('total_emissions')

# print(sector_pollutant_agg.head(10))

# sector_source_pollutant_agg = \
# sectoral_emissions_fil.group_by(['sector', 'source', 'pollutant']).agg(
#     pl.col('emissions').sum().alias('total_emissions')
# ).sort('total_emissions', descending=True)

# print(sector_source_pollutant_agg.head(10))
