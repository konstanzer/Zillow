import pandas as pd
import numpy as np
from scipy import stats

import geopandas as gpd
from shapely.geometry import Point, Polygon

from sklearn.model_selection import train_test_split


def wrangle_zillow(df, k=1.5):
    
    df=df.rename(columns={'calculatedfinishedsquarefeet':'finishedsqft',
                          'lotsizesquarefeet':'lotsqft',
                          'structuretaxvaluedollarcnt':'structuretaxvalue',
                          'yearbuilt':'year', 'taxvaluedollarcnt':'taxvalue',
                          'landtaxvaluedollarcnt':'landtaxvalue',
                          'longitude/1e6':'longitude', 'latitude/1e6':'latitude'})
    
    df['year'].fillna(np.nanmedian(df.year), inplace=True)
    df['finishedsqft'].fillna(np.nanmedian(df.finishedsqft), inplace=True)
    df['lotsqft'].fillna(np.nanmedian(df.lotsqft), inplace=True)
    
    #engineered to show what proportion of lot is finished space 
    df['livingarearatio'] = df.finishedsqft/df.lotsqft 
    
    df['bedroomcnt'].replace(0, np.median(df.bedroomcnt), inplace=True)
    df['bathroomcnt'].replace(0, np.median(df.bathroomcnt), inplace=True)
    df['roomcnt'].replace(0, df.bedroomcnt+df.bathroomcnt+2, inplace=True)
    
    #if any other columns are missing, drop it
    df=df.dropna(axis=0)
    
    #engineered to show what proportion building is of total value
    df['buildinglandvalueratio'] = df.structuretaxvalue/df.landtaxvalue 
    
    #handling outliers assuming no distribution
    cols = ['taxvalue', 'taxamount', 'finishedsqft', 'taxrate', 'structuretaxvalue']
    df = iqr_method(df, k, cols)
        
    int_cols = ['fips', 'bedroomcnt', 'bathroomcnt', 'taxvalue', 'taxamount', 'roomcnt',
                'finishedsqft', 'year', 'structuretaxvalue', 'landtaxvalue', 'lotsqft']
    df[int_cols] = df[int_cols].astype('int')
    
    counties = {6111:"Ventura", 6037:"Los Angeles", 6059:"Orange"}
    df['county'] = df.fips.map(counties)
    
    y = df.pop('taxvalue')
    
    return split_data(df, y, .15)


def iqr_method(df, k, cols):
    
    #drop row if column outside fences
    #k is usu. between 1.5 and 3
    for col in cols:
        
        q1, q3 = df[col].quantile([.25,.75])
        iqr = q3-q1
        upperbound, lowerbound = q3 + k*iqr, q1 - k*iqr
        df = df[(df[col] > lowerbound) & (df[col] < upperbound)]
        
    return df


def z_score_method(df, cols):
    
    #drop row if column has a z-score over 3, must be normal
    for col in cols:
        df = df[(np.abs(stats.zscore(df[col])) < 3)]
        
    return df
    
    
def split_data(X, y, test_size):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=36)
    test_size2 = test_size/(1-test_size)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=test_size2, random_state=36)
    print("X_train, X_test, X_val, y_train, y_test, y_val")
    print(X_train.shape, X_test.shape, X_val.shape, y_train.shape, y_test.shape, y_val.shape)
    
    return X_train, X_test, X_val, y_train, y_test, y_val


def geo_df(df, y, file):
    map_ = gpd.read_file(file)
    geom = [Point(xy) for xy in zip(df.longitude, df.latitude)]
    df['taxvalue'] = y
    geo_df = gpd.GeoDataFrame(df, crs = {'init':'epsg:4326'}, geometry=geom)
    
    return geo_df, map_