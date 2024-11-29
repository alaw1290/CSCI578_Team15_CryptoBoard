# CSCI578_Team15_CryptoBoard

# 1. Packages installed so far:

pip3 install requests
pip3 install psycopg2
pip3 install flask
pip3 install bs4

# 2. Create a .env file with the attributes below:

DB_NAME=cryptoboard
DB_USER=cryptoboard_owner
DB_PASSWORD=PASSWORD
DB_HOST=HOST_ADDRESS
DB_SSLMODE=require
DB_SSLROOTCERT=/path/to/root.crt

# 3. Run:

python3 app.py
http://127.0.0.1:8000/crawl?sourceName=nytimes.com&cryptoName=Bitcoin&number=30

News Sources:
http://127.0.0.1:8000/crawl?sourceName=cnn.com&cryptoName=Bitcoin&number=100
http://127.0.0.1:8000/crawl?sourceName=foxnews.com&cryptoName=Bitcoin&number=100

Social Media:
http://127.0.0.1:8000/crawl?sourceName=reddit.com&cryptoName=Bitcoin&number=100


# Docker setup

Run `docker compose up --build` to start the flask app and postgres database. By default, the postgres database will be on port 5432 and flask will be on port 8000.
