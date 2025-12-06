import polars as pl

#clean the sectoral emissions 
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