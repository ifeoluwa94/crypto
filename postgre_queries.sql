-- postgre instance connection details
-- host: 34.105.201.48
-- database: crypto_db
-- user: postgres
-- password: 12345

-- Create the e currencies table in the db and set currency code as primary key
CREATE TABLE currencies 
(
	currency_id SERIAL ,
	currency_code VARCHAR(255) NOT NULL PRIMARY KEY,
	currency_name VARCHAR(255) NOT NULL 
);

-- Create the currency history table based on json structure returned from API and set the currency code as foreign key to ensure one-to-many relationship with currency table
CREATE TABLE history 
(
	id SERIAL,
	currency_code VARCHAR(255) FOREIGN KEY,
	time_period_end VARCHAR(255)  NOT NULL,
	time_period_start VARCHAR(255)  NOT NULL,
	time_open VARCHAR(255)  NOT NULL,
	time_close VARCHAR(255)  NOT NULL,
	price_open VARCHAR(255)  NOT NULL,
	price_high VARCHAR(255)  NOT NULL,
	price_low VARCHAR(255)  NOT NULL,
	price_close VARCHAR(255)  NOT NULL,
	volume_traded VARCHAR(255)  NOT NULL,
	trades_count VARCHAR(255)  NOT NULL
);

-- Insert currency details in currency table
INSERT INTO currencies (currency_code, currency_name)
VALUES
	('BTC','Bitcoin'),
	('ETH','Ethereum'),
	('XRP','Ripple'),
	('LTC','Litecoin');
	

