#-------------------------------------
# PART 1 -----------------------------
#-------------------------------------

# Create a script in Python that given a cryptocurrency symbol (i.e. BTC), that returns the historical data fetched from the API.

crypto = 'BTC' #  assign required crypto currency symbol 
Date = '2016-01-01' # Start date
CDate = '2020-05-13' # Stop date
all_crypto_history = [] # create empty list object list to be used to persist batch result from API response

# Load the data from the API for given crpto currency until current data 'CDATE' and persist batch result in list object
while Date != CDate:	
	url = 'https://rest.coinapi.io/v1/ohlcv/'+crypto+'/USD/history?period_id=1DAY&time_start='+Date # batch load daily currency history from API
	headers = {'X-CoinAPI-Key' : '669314B7-AC6A-43D5-A818-B4C8DE0AA149'}   
	response = requests.get(url, headers=headers)
	lent = len(response.json())
	all_crypto_hist = response.json() # retrieve batch result from API
	Date = all_crypto_hist[lent-1]['time_period_end'][0:10] # obtain end date in batch retrieved from API 
	all_crypto_history.append(all_crypto_hist) # persist batch result into a list


#-------------------------------------
# PART 2 -----------------------------
#-------------------------------------


# Postgress DB instance created on GCP CLoud SQl: See connection details below

#-- postgre instance connection details
#-- host: 34.105.201.48
#-- database: crypto_db
#-- user: postgres
#-- password: 12345

# commands to create required tables below

#-- Create the e currencies table in the db and set currency code as primary key
#CREATE TABLE currencies 
#(
#	currency_id SERIAL ,
#	currency_code VARCHAR(255) NOT NULL PRIMARY KEY,
#	currency_name VARCHAR(255) NOT NULL 
#);

#---Load data into currency table
# Insert currency details in currency table
# INSERT INTO currencies (currency_code, currency_name)
#VALUES
#	('BTC','Bitcoin'),
#	('ETH','Ethereum'),
#	('XRP','Ripple'),
#	('LTC','Litecoin');
	

#-- Create the currency history table based on json structure returned from API and set the currency code as foreign key to ensure one-to-many relationship with currency table
#CREATE TABLE history 
#(
#	id SERIAL,
#	currency_code VARCHAR(255) FOREIGN KEY,
#	time_period_end VARCHAR(255)  NOT NULL,
#	time_period_start VARCHAR(255)  NOT NULL,
#	time_open VARCHAR(255)  NOT NULL,
#	time_close VARCHAR(255)  NOT NULL,
#	price_open VARCHAR(255)  NOT NULL,
#	price_high VARCHAR(255)  NOT NULL,
#	price_low VARCHAR(255)  NOT NULL,
#	price_close VARCHAR(255)  NOT NULL,
#	volume_traded VARCHAR(255)  NOT NULL,
#	trades_count VARCHAR(255)  NOT NULL
#);

import psycopg2 #  PostgreSQL database adapter for Python
conn = psycopg2.connect(host="34.105.201.48",database="crypto_db", user="postgres", password="12345")  # create connection instance to postgre DB

# load all required data for all cryptocurrency specified into the history table
Date = '2016-01-01'
CDate = '2020-05-13'
all_crypto_history = [] # create empty list object list to be used to persist batch result from API response
lent = 100
crypto_list = ['BTC','ETH','XRP','LTC'] # list object containing symbol of all required crypto currency
for crypto in crypto_list: # iterate over all currency 
    while Date != CDate:
        url = 'https://rest.coinapi.io/v1/ohlcv/'+crypto+'/USD/history?period_id=1DAY&time_start='+Date
        headers = {'X-CoinAPI-Key' : '669314B7-AC6A-43D5-A818-B4C8DE0AA149'}   
        response = requests.get(url, headers=headers)
        lent = len(response.json()) # update lent object to current lenght of response from API call
        all_crypto_hist = response.json() # retrieve batch result from API
        Date = all_crypto_hist[lent-1]['time_period_end'][0:10] # obtain end date in batch retrieved from API 
        all_crypto_history.append(all_crypto_hist) # persist batch result into a list object
        
    for a in range(len(all_crypto_history)):
        for b in range(len(all_crypto_history[a])):
            mydict = all_crypto_history[a][b]
            #columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in mydict.keys())+',`currency_code`'
            columns = ', '.join( str(x).replace('/', '_') for x in mydict.keys())+',currency_code'
            values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in mydict.values())+','+"'"+crypto+"'"
            #values = ', '.join(str(x).replace('/', '_') for x in mydict.values())+',BTC'
            sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('history', columns, values) 
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit() 
    # Re-initialize below objects for next currency batch export and load
    Date = '2016-01-01'
    CDate = '2020-05-13'
    all_crypto_history = []
    lent = 100


#-------------------------------------
# PART 3 -----------------------------
#-------------------------------------