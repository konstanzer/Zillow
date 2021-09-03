import pandas as pd

try: from env import host, username, password
except: from src.env import host, username, password


def get_db_url(username, host, password, db):
    return f'mysql+pymysql://{username}:{password}@{host}/{db}'

def get_zillow_data():
	url = get_db_url(username, host, password, 'zillow')
	#261 is code for single-family property
	query = """
		SELECT parcelid, transactiondate, latitude/1e6, longitude/1e6, bedroomcnt, roomcnt,
                bathroomcnt, calculatedfinishedsquarefeet, lotsizesquarefeet,
                taxvaluedollarcnt, yearbuilt, taxamount, taxamount/taxvaluedollarcnt taxrate,
                fips, structuretaxvaluedollarcnt, landtaxvaluedollarcnt
		FROM properties_2017
		JOIN predictions_2017 USING(parcelid)
		WHERE propertylandusetypeid = 261
            AND transactiondate BETWEEN '2017-05-01' AND '2017-08-31';
		"""
	return pd.read_sql(query, url)

    
if __name__ == '__main__':
	zillow = get_zillow_data()
	print(zillow.head())
	print(zillow.info())
	print(zillow.describe())