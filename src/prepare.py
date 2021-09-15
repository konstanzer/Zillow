import pandas as pd
import numpy as np
from scipy import stats

import geopandas as gpd
from shapely.geometry import Point, Polygon

from sklearn.model_selection import train_test_split


def wrangle_zillow(df, test_size=.15, random_state=0, k=1.5):
    
    df=df.rename(columns={'calculatedfinishedsquarefeet':'finishedsqft',
                          'lotsizesquarefeet':'lotsqft',
                          'structuretaxvaluedollarcnt':'structuretaxvalue',
                          'yearbuilt':'year', 'taxvaluedollarcnt':'taxvalue',
                          'landtaxvaluedollarcnt':'landtaxvalue'})
    
    for col in df.columns:
        try:
            df[col].fillna(np.nanmedian(df[col]), inplace=True)
        except:
            continue

    df['bedroomcnt'].replace(0, np.median(df.bedroomcnt), inplace=True)
    df['bathroomcnt'].replace(0, np.median(df.bathroomcnt), inplace=True)
    
    #if MVP columns are missing, drop it
    df=df.dropna(axis=0, subset=["taxvalue", "finishedsqft"])

    #engineered to show what proportion of lot is finished space 
    df['livingarearatio'] = df.finishedsqft/df.lotsqft 
    
    #engineered to show what proportion building is of total value
    #df['buildinglandvalueratio'] = df.structuretaxvalue/df.landtaxvalue 
    df['taxrate'] = df.taxamount/df.taxvalue 

    df.latitude, df.longitude = df.latitude/1e6, df.longitude/1e6
    
    #handling outliers assuming no distribution
    cols = ['taxvalue', 'taxamount', 'taxrate']
    df = iqr_method(df, k, cols)
        
    int_cols = ['fips', 'bedroomcnt', 'bathroomcnt', 'taxvalue', 'taxamount',
                'finishedsqft', 'year', 'structuretaxvalue', 'landtaxvalue',
                'lotsqft', 'regionidzip']
    df[int_cols] = df[int_cols].astype('int')
    
    counties = {6111:"Ventura", 6037:"Los Angeles", 6059:"Orange"}
    df['county'] = df.fips.map(counties)
    
    #why not?
    zipzies = pd.get_dummies(df.regionidzip)
    #counties = pd.get_dummies(df.county)
    
    df = pd.concat([df, zipzies], axis=1)
    df=df.drop(columns=['fips'])
    y = df.pop('taxvalue')
    
    return split_data(df, y, test_size, random_state)


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
    
    
def split_data(X, y, test_size, random_state):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    test_size2 = test_size/(1-test_size)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=test_size2, random_state=random_state)
    print("X_train, X_test, X_val, y_train, y_test, y_val")
    print(X_train.shape, X_test.shape, X_val.shape, y_train.shape, y_test.shape, y_val.shape)
    
    return X_train, X_test, X_val, y_train, y_test, y_val


def geo_df(df, y, file):
    map_ = gpd.read_file(file)
    geom = [Point(xy) for xy in zip(df.longitude, df.latitude)]
    geo_df = gpd.GeoDataFrame(df, crs = {'init':'epsg:4326'}, geometry=geom)
    
    return geo_df, map_