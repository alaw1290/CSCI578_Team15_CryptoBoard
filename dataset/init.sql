SET DateStyle TO ISO;

CREATE TABLE coinmarket_id_map (
    Coinmarket_ID Int,
    Name Text,
    Symbol Text
);

COPY coinmarket_id_map
FROM '/docker-entrypoint-initdb.d/coinmarket_id_map.csv'
DELIMITER ','
CSV HEADER;

CREATE TABLE coinmarket_data (
    coinmarket_id Int, 
    name Text, 
    symbol Text,
    slug Text,
    max_supply Bigint, 
    infinite_supply Boolean, 
    price Decimal, 
    market_cap Decimal, 
    total_supply Decimal, 
    volume_24h Decimal, 
    percent_change_1h Decimal,
    percent_change_24h Decimal,
    percent_change_7d Decimal,
    percent_change_30d Decimal,
    circulating_supply Decimal,
    data_timestamp timestamp
);

COPY coinmarket_data
FROM '/docker-entrypoint-initdb.d/coinmarket_data.csv'
DELIMITER ','
CSV HEADER;

CREATE TABLE stored_urls (
    crypto_name Text, 
    source Text,
    url Text,
    id Int, 
    title Text, 
    published_date Text, 
    summary Text
);

COPY stored_urls
FROM '/docker-entrypoint-initdb.d/stored_urls.csv'
DELIMITER ','
CSV HEADER;


CREATE TABLE stored_urls_sentiment (
    id Int, 
    sentiment Int
);

COPY stored_urls_sentiment
FROM '/docker-entrypoint-initdb.d/stored_urls_sentiment.csv'
DELIMITER ','
CSV HEADER;