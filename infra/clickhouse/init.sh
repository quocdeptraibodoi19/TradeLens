#!/bin/bash
set -e

CH_HOST="${CH_HOST:-localhost}"
CH_PORT="${CH_PORT:-8123}"
CH_CLUSTER="${CH_CLUSTER:-cluster_2S_2R}"

ch_query() {
    curl -sf "http://${CH_HOST}:${CH_PORT}/" \
        -u "default:" \
        --data "$1"
}

echo "Waiting for ClickHouse to be ready..."
until ch_query "SELECT 1" > /dev/null 2>&1; do
    sleep 2
done

echo "Creating database..."
ch_query "CREATE DATABASE IF NOT EXISTS ${CH_DATABASE} ON CLUSTER ${CH_CLUSTER}"

echo "Creating admin user..."
ch_query "CREATE USER IF NOT EXISTS ${CH_ADMIN_USER}
    IDENTIFIED WITH sha256_password BY '${CH_ADMIN_PASSWORD}'
    ON CLUSTER ${CH_CLUSTER}"

ch_query "GRANT ALL ON *.* TO ${CH_ADMIN_USER}
    WITH GRANT OPTION
    ON CLUSTER ${CH_CLUSTER}"

echo "Creating app service account..."
ch_query "CREATE USER IF NOT EXISTS ${CH_USER}
    IDENTIFIED WITH sha256_password BY '${CH_PASSWORD}'
    ON CLUSTER ${CH_CLUSTER}"

ch_query "GRANT SELECT, INSERT ON ${CH_DATABASE}.* TO ${CH_USER}
    ON CLUSTER ${CH_CLUSTER}"

echo "Done."
