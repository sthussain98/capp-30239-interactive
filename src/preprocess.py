import polars as pl
import geojson


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

def clean_aqi():
    """
    This function loads the raw AQI data and cleans as following: 
    1. Keeps data only for Lahore
    2. Cleans the timestamp variablto extract year and month
    3. Ensures latitude and longitude are read as numeric values
    4. Generates monthly averages of AQI readings from each monitor
    5. Categorizes readings
    """
    aqi_data = pl.read_csv("../data/AQI_data.csv")
    aqi_data_lhe = aqi_data.filter(pl.col('city') == 'Lahore')
    aqi_data_lhe_clean = aqi_data_lhe.with_columns(pl.col('timestamp')
                                         .str.split('-')
                                         .alias('date_split')).with_columns(
                                             pl.col("date_split").list.get(0).alias('year'), 
                                             pl.col('date_split').list.get(1).alias('month')
                                         ).with_columns(pl.col('month')
                                                        .replace(month_map)
                                                        .alias("full_month_name")
                                         ).drop('date_split').filter(pl.col("us_aqi").is_not_null())
    
    aqi_data_lhe_clean = aqi_data_lhe_clean.with_columns(
        pl.col('latitude').cast(pl.Float64),
        pl.col('longitude').cast(pl.Float64)
    )

    aqi_data_lhe_clean = aqi_data_lhe_clean.drop_nulls(["longitude", "latitude"])
    # generate monthly averages of AQI readings for a monitor
    aqi_mon_avg = aqi_data_lhe_clean.group_by(['station_name', 
                                           'latitude', 
                                           'longitude', 
                                           'year', 
                                           'full_month_name'
                                           ]).agg(
                                               pl.col('us_aqi').mean().alias('avg_aqi')
                                           ).sort('avg_aqi', descending = True)
    
    aqi_mon_avg_cat = aqi_mon_avg.with_columns(
        pl.when(pl.col('avg_aqi') <= 50).then(pl.lit('Good'))
        .when((pl.col('avg_aqi') > 50) & (pl.col('avg_aqi') <= 100)).then(pl.lit('Moderate'))
        .when((pl.col('avg_aqi') > 100) & (pl.col('avg_aqi') <= 150)).then(pl.lit('Unhealthy for Sensitive Groups'))
        .when((pl.col('avg_aqi') > 150) & (pl.col('avg_aqi') <= 200)).then(pl.lit('Unhealthy'))
        .when((pl.col('avg_aqi') > 200) & (pl.col('avg_aqi') <= 300)).then(pl.lit('Very Unhealthy'))
        .when(pl.col('avg_aqi') > 300).then(pl.lit('Hazardous'))
        .otherwise(pl.lit('NA'))
        .alias('aqi_cat'))
    
    return aqi_mon_avg_cat


def gen_geojson(df):
    """
    This function generates a geojson of the AQI data
    """
    features = []
    for row in df.iter_rows(named = True):
        lon = round(row["longitude"], 4)
        lat = round(row["latitude"], 4)
        feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lon, lat]
        },
        "properties": {
            "avg_aqi": row["avg_aqi"],
            "year": row["year"], 
            "month": row["full_month_name"], 
            "station_name": row["station_name"], 
            "aqi_cat": row["aqi_cat"]
        }
    }
        features.append(feature)
    geojson_obj = geojson.FeatureCollection(features)
    with open('../data/aqi_lhe_data.geojson', 'w') as f:
        geojson.dump(geojson_obj, f)

#gen_geojson(clean_aqi())
