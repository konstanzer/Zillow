import pandas as pd

try: from env import host, username, password
except: from src.env import host, username, password


def get_db_url(username, host, password, db):
    return f'mysql+pymysql://{username}:{password}@{host}/{db}'

def get_zillow_data():
    url = get_db_url(username, host, password, 'zillow')
    query = """
    SELECT bathroomcnt, bedroomcnt, buildingqualitytypeid,
        calculatedfinishedsquarefeet, yearbuilt, fips, lotsizesquarefeet, regionidzip,
        structuretaxvaluedollarcnt, landtaxvaluedollarcnt, latitude, longitude,
        taxamount, taxvaluedollarcnt
    FROM properties_2017
    JOIN predictions_2017 USING(parcelid)
    WHERE propertylandusetypeid IN (260,261,262,263,264,265,266,275)
        AND transactiondate BETWEEN '2017-05-01' AND '2017-08-31';
    """
    return pd.read_sql(query, url)

    
if __name__ == '__main__':
	zillow = get_zillow_data()
	print(zillow.head())
	print(zillow.info())
	print(zillow.describe())