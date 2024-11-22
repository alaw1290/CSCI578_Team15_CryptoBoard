CREATE TABLE coinmarket_id_map (
    ID Int,
    Name TEXT,
    Symbol TEXT
);

COPY coinmarket_id_map
FROM '/docker-entrypoint-initdb.d/coinmarket_id_map.csv'
DELIMITER ','
CSV HEADER;
