#!/bin/bash
set -e

# Create the Odoo user and database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    CREATE USER odoo WITH PASSWORD 'admin123';
    CREATE DATABASE odoo OWNER odoo;
    GRANT ALL PRIVILEGES ON DATABASE odoo TO odoo;
EOSQL

echo "Database initialization completed successfully"
