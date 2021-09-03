import pandas as pd
import numpy as np
from scipy import stats

import geopandas as gpd
from shapely.geometry import Point, Polygon

from sklearn.model_selection import train_test_split


def wrangle_zillow(df):
    
    df=df.rename(columns={'calculatedfinishedsquarefeet':'sqft',
                       'yearbuilt':'year', 'taxvaluedollarcnt':'taxvalue',
                       'longitude/1e6':'longitude', 'latitude/1e6':'latitude'})
    
    df['year'].fillna(np.nanmedian(df.year), inplace=True)
    df['sqft'].fillna(np.nanmedian(df.sqft), inplace=True)
    
    df['bedroomcnt'].replace(0, np.median(df.bedroomcnt), inplace=True)
    df['bathroomcnt'].replace(0, np.median(df.bathroomcnt), inplace=True)
    
    df=df.dropna(axis=0)
    
    cols = ['taxvalue', 'taxamount', 'sqft', 'taxrate']
    #drop row if column has a z-score over 3
    for col in cols:
        df = df[(np.abs(stats.zscore(df[col])) < 3)]
        
    int_cols = ['fips', 'bedroomcnt', 'bathroomcnt', 'taxvalue', 'taxamount', 'sqft', 'year']
    df[int_cols] = df[int_cols].astype('int')
    
    counties = {6111:"Ventura", 6037:"Los Angeles", 6059:"Orange"}
    df['county'] = df.fips.map(counties)
    
    return df

def split_data(X, y, test_size):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=36)
    test_size2 = test_size/(1-test_size)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=test_size2, random_state=36)
    print("X_train, X_test, X_val, y_train, y_test, y_val")
    print(X_train.shape, X_test.shape, X_val.shape, y_train.shape, y_test.shape, y_val.shape)
    
    return X_train, X_test, X_val, y_train, y_test, y_val


def geo_df(df, file):
    map_ = gpd.read_file(file)
    geom = [Point(xy) for xy in zip(df.longitude, df.latitude)]
    geo_df = gpd.GeoDataFrame(df, crs = {'init':'epsg:4326'}, geometry=geom)
    
    return geo_df, map_