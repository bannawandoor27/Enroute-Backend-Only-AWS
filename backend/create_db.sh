#!/bin/bash

set -e

# Start the PostgreSQL service
service postgresql start

# Create the user and database
psql -U postgres -c "CREATE USER postgres WITH PASSWORD 'banna';"
psql -U postgres -c "CREATE DATABASE enroute;"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE enroute TO postgres;"

# Stop the PostgreSQL service
service postgresql stop
