#!/usr/bin/env sh

set -o errexit
set -o nounset

cmd="$*"

if test "${DB_DEFAULT_ENGINE#*sqlite}" = "$DB_DEFAULT_ENGINE"; then
	db_1_ready() {
		dockerize -wait "tcp://$DB_DEFAULT_HOST:$DB_DEFAULT_PORT"
	}

	until db_1_ready; do
		echo >&2 'DB default is unavailable - sleeping'
	done

	echo >&2 'DB default is up - continuing...'
fi

if test "${DB_JAVA_WALLET_ENGINE#*sqlite}" = "$DB_JAVA_WALLET_ENGINE"; then
	db_2_ready() {
		dockerize -wait "tcp://$DB_JAVA_WALLET_HOST:$DB_JAVA_WALLET_PORT"
	}

	until db_2_ready; do
		echo >&2 'DB wallet is unavailable - sleeping'
	done

	echo >&2 'DB wallet is up - continuing...'
fi

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd
