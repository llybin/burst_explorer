#!/usr/bin/env sh

set -o errexit
set -o nounset

cmd="$*"

if [ -n "$DB_DEFAULT_HOST" ]; then
    mysql_1_ready() {
        dockerize -wait "tcp://$DB_DEFAULT_HOST:$DB_DEFAULT_PORT" -timeout 5s
    }

    until mysql_1_ready; do
        echo >&2 'Mysql defaul is unavailable - sleeping'
    done

    echo >&2 'Mysql default is up - continuing...'
fi

if [ -n "$DB_JAVA_WALLET_HOST" ]; then
    mysql_2_ready() {
        dockerize -wait "tcp://$DB_JAVA_WALLET_HOST:$DB_JAVA_WALLET_PORT" -timeout 5s
    }

    until mysql_2_ready; do
        echo >&2 'Mysql wallet is unavailable - sleeping'
    done

    echo >&2 'Mysql wallet is up - continuing...'
fi

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd
