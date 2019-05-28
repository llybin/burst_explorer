# BurstCoin Blockchain Explorer

[![Build Status](https://travis-ci.com/llybin/burst_explorer.svg?branch=master)](https://travis-ci.com/llybin/burst_explorer)
[![GPLv3](https://img.shields.io/badge/license-GPLv3-blue.svg)](LICENSE)

## Donations

BURST-D372-C2DU-HMKK-CQLHA

## How to run

See additional info about set up DB [here](java_wallet)

### Development

`docker-compose up`

### Production

`cp .env.default .env`

Configure your .env:

```
DEBUG=False
SECRET_KEY= set up
DB_DEFAULT_URL= set up
DB_JAVA_WALLET_URL= set up
```

`docker-compose up`
