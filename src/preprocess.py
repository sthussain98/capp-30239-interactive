import polars as pl
import geojson

# Clean the AQI data
# read the data


# # filter to only lahore



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


# generate a test geojson for 1 year

#test_df = clean_aqi()
#test_df.write_csv('../data/test.csv')
#print(test_df.filter(pl.col('station_name') == 'WWF-PAKISTAN').tail(10))

#years = test_df.select(pl.col('year')).unique().to_series().to_list()

def gen_geojson(df):
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


# clean the sectoral emissions 
pol_lst = ['PM2.5', 'SOx', 'NOx', 'CO']

def clean_sector_emissions():
    sectoral_emissions = pl.read_csv("../data/sectoral_data_lhe.csv")
    sectoral_emissions_fil = sectoral_emissions.filter(pl.col('pollutant')
                                                       .is_in(pol_lst))
    
    sectoral_emissions_fil = sectoral_emissions_fil.with_columns(
    pl.when(pl.col('source') == "Charcoal").then(pl.lit("Coal"))
     .when(pl.col('source') == "NG").then(pl.lit("Natural Gas"))
     .when(pl.col('source') == "Gas").then(pl.lit("Natural Gas"))
     .otherwise(pl.col('source'))
     .alias("source"))
    
    return sectoral_emissions_fil


def sector_aggregates(df): 
    sector_aggregates = df.group_by('sector').agg(
    pl.col('emissions').sum().alias('total_emissions')
)
    return sector_aggregates


def sector_pollutant_aggregates(df): 
    sector_pollutant_agg = \
        df.group_by(['sector', 'pollutant']).agg(
            pl.col('emissions').sum().alias('total_emissions')
            ).sort('total_emissions')
    return sector_pollutant_agg

def sector_source_pollutant_aggregates(df):
    sector_source_pollutant_agg = \
        df.group_by(['sector', 'source', 'pollutant']).agg(
            pl.col('emissions').sum().alias('total_emissions')
            ).sort('total_emissions', descending=True)
    
    df_sector_source = sector_source_pollutant_agg.with_columns(
        pl.concat_str(['sector', 'source'], separator= '/').alias("sector_source")

    )
    return df_sector_source

def sector_source_aggregates(df):
    sector_source_agg = \
    df.group_by(['sector', 'source']).agg(
        pl.col('emissions').sum().alias('total_emissions'))
    return sector_source_agg

def source_pollutant_aggregates(df):
    source_pollutant_agg = \
    df.group_by(['source', 'pollutant']).agg(
        pl.col('emissions').sum().alias('total_emissions'))
    return source_pollutant_agg 



# df = sector_source_pollutant_aggregates(clean_sector_emissions())
sector_source = sector_source_aggregates(clean_sector_emissions())
sector_source.write_csv('../data/sector_source_aggregates.csv')

source_pollutant = source_pollutant_aggregates(clean_sector_emissions())
source_pollutant.write_csv('../data/source_pollutant_aggregates.csv')
# #df.write_csv('sector_source_pollutant_aggregates.csv')



#print(sector_source_pollutant_aggregates(clean_sector_emissions()).head(20))