
I am a data scientist at Zillow. This morning, I received the following email:

	We want to be able to predict the values of single-unit properties that the tax district assesses using the property data from those with a transaction during the "hot months" of May-August 2017.

	Property taxes are assessed at the county level. The data has the tax amounts and tax value of the home so it shouldn't be too hard to calculate. Please include in your report to us the distribution of tax rates for each county so that we can see how much they vary within the properties in the county and the rates most properties hover around.

	This is separate from the model you will build because, if you use tax amount in your model, you would be using a future data point to predict a future data point. For prediction purposes, we won't know tax amount until we know tax value.

Audience: Zillow data team

Goals:
* Predict values of tax-assessed, single-unit properties bought or sold between May and August 2017. (Exclude tax amount from model.)
* Label properties' states and counties via tax rates calculated using tax values and tax amounts.
* Report tax rate distributions by county.


Artifacts:
* slides w/ drivers of single-unit property values - for 5 min presentation
* repo notebook w/ pipeline, 2 t-tests + viz, baseline and model, address email
* readme w/ reproduction instructions, goals, data dict, takeaways

| Feature                        | Description                                                                                                            |
|--------------------------------|------------------------------------------------------------------------------------------------------------------------|
| 'airconditioningtypeid'        |  Type of cooling system present in the home (if any)                                                                   |
| 'architecturalstyletypeid'     |  Architectural style of the home (i.e. ranch, colonial, split-level, etc…)                                             |
| 'basementsqft'                 |  Finished living area below or partially below ground level                                                            |
| 'bathroomcnt'                  |  Number of bathrooms in home including fractional bathrooms                                                            |
| 'bedroomcnt'                   |  Number of bedrooms in home                                                                                            |
| 'buildingqualitytypeid'        |  Overall assessment of condition of the building from best (lowest) to worst (highest)                                 |
| 'buildingclasstypeid'          | The building framing type (steel frame, wood frame, concrete/brick)                                                    |
| 'calculatedbathnbr'            |  Number of bathrooms in home including fractional bathroom                                                             |
| 'decktypeid'                   | Type of deck (if any) present on parcel                                                                                |
| 'threequarterbathnbr'          |  Number of 3/4 bathrooms in house (shower + sink + toilet)                                                             |
| 'finishedfloor1squarefeet'     |  Size of the finished living area on the first (entry) floor of the home                                               |
| 'calculatedfinishedsquarefeet' |  Calculated total finished living area of the home                                                                     |
| 'finishedsquarefeet6'          | Base unfinished and finished area                                                                                      |
| 'finishedsquarefeet12'         | Finished living area                                                                                                   |
| 'finishedsquarefeet13'         | Perimeter  living area                                                                                                 |
| 'finishedsquarefeet15'         | Total area                                                                                                             |
| 'finishedsquarefeet50'         |  Size of the finished living area on the first (entry) floor of the home                                               |
| 'fips'                         |  Federal Information Processing Standard code -  see https://en.wikipedia.org/wiki/FIPS_county_code for more details   |
| 'fireplacecnt'                 |  Number of fireplaces in a home (if any)                                                                               |
| 'fireplaceflag'                |  Is a fireplace present in this home                                                                                   |
| 'fullbathcnt'                  |  Number of full bathrooms (sink, shower + bathtub, and toilet) present in home                                         |
| 'garagecarcnt'                 |  Total number of garages on the lot including an attached garage                                                       |
| 'garagetotalsqft'              |  Total number of square feet of all garages on lot including an attached garage                                        |
| 'hashottuborspa'               |  Does the home have a hot tub or spa                                                                                   |
| 'heatingorsystemtypeid'        |  Type of home heating system                                                                                           |
| 'latitude'                     |  Latitude of the middle of the parcel multiplied by 10e6                                                               |
| 'longitude'                    |  Longitude of the middle of the parcel multiplied by 10e6                                                              |
| 'lotsizesquarefeet'            |  Area of the lot in square feet                                                                                        |
| 'numberofstories'              |  Number of stories or levels the home has                                                                              |
| 'parcelid'                     |  Unique identifier for parcels (lots)                                                                                  |
| 'poolcnt'                      |  Number of pools on the lot (if any)                                                                                   |
| 'poolsizesum'                  |  Total square footage of all pools on property                                                                         |
| 'pooltypeid10'                 |  Spa or Hot Tub                                                                                                        |
| 'pooltypeid2'                  |  Pool with Spa/Hot Tub                                                                                                 |
| 'pooltypeid7'                  |  Pool without hot tub                                                                                                  |
| 'propertycountylandusecode'    |  County land use code i.e. it's zoning at the county level                                                             |
| 'propertylandusetypeid'        |  Type of land use the property is zoned for                                                                            |
| 'propertyzoningdesc'           |  Description of the allowed land uses (zoning) for that property                                                       |
| 'rawcensustractandblock'       |  Census tract and block ID combined - also contains blockgroup assignment by extension                                 |
| 'censustractandblock'          |  Census tract and block ID combined - also contains blockgroup assignment by extension                                 |
| 'regionidcounty'               | County in which the property is located                                                                                |
| 'regionidcity'                 |  City in which the property is located (if any)                                                                        |
| 'regionidzip'                  |  Zip code in which the property is located                                                                             |
| 'regionidneighborhood'         | Neighborhood in which the property is located                                                                          |
| 'roomcnt'                      |  Total number of rooms in the principal residence                                                                      |
| 'storytypeid'                  |  Type of floors in a multi-story house (i.e. basement and main level, split-level, attic, etc.).  See tab for details. |
| 'typeconstructiontypeid'       |  What type of construction material was used to construct the home                                                     |
| 'unitcnt'                      |  Number of units the structure is built into (i.e. 2 = duplex, 3 = triplex, etc...)                                    |
| 'yardbuildingsqft17'           | Patio in  yard                                                                                                         |
| 'yardbuildingsqft26'           | Storage shed/building in yard                                                                                          |
| 'yearbuilt'                    |  The Year the principal residence was built                                                                            |
| 'taxvaluedollarcnt'            | The total tax assessed value of the parcel                                                                             |
| 'structuretaxvaluedollarcnt'   | The assessed value of the built structure on the parcel                                                                |
| 'landtaxvaluedollarcnt'        | The assessed value of the land area of the parcel                                                                      |
| 'taxamount'                    | The total property tax assessed for that assessment year                                                               |
| 'assessmentyear'               | The year of the property tax assessment                                                                                |
| 'taxdelinquencyflag'           | Property taxes for this parcel are past due as of 2015                                                                 |
| 'taxdelinquencyyear'           | Year for which the unpaid propert taxes were due                                                                       |

Data: properties_2017 and predictions_2017
MVP X-variables: square feet of the home, number of bedrooms, number of bathrooms for target, property's assessed value aka taxvaluedollarcnt
