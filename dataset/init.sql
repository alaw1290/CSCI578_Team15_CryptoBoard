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
    id Text, 
    coinmarket_id Int, 
    name Text, 
    symbol Text,
    slug Text,
    max_supply Bigint, 
    circulating_supply Decimal, 
    total_supply Decimal, 
    infinite_supply Boolean, 
    cmc_rank Bigint, 
    USD_quote Decimal, 
    USD_market_cap Decimal,
    last_updated Text
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