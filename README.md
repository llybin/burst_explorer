# BurstCoin Blockchain Explorer

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f37cb0ffe26f4a88b12d12fb602c5ab2)](https://app.codacy.com/app/llybin/burst_explorer?utm_source=github.com&utm_medium=referral&utm_content=llybin/burst_explorer&utm_campaign=Badge_Grade_Dashboard)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/7fe1f95f5ef141e1ad5fe963cc88c825)](https://www.codacy.com/app/llybin/burst_explorer?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=llybin/burst_explorer&amp;utm_campaign=Badge_Coverage)
[![Build Status](https://travis-ci.com/llybin/burst_explorer.svg?branch=master)](https://travis-ci.com/llybin/burst_explorer)
[![GPLv3](https://img.shields.io/badge/license-GPLv3-blue.svg)](LICENSE)

## Donations

**BURST-D372-C2DU-HMKK-CQLHA**

## How to run

See additional info about set up DB [here](java_wallet)

### Development

`docker-compose up service`

`docker-compose up autotests`

### Production

`cp .env.default .env`

Configure your .env:

See [url-schema](https://github.com/kennethreitz/dj-database-url#url-schema) for set up.

``` console
DEBUG=False
SECRET_KEY= set up
DB_DEFAULT_URL= set up
DB_JAVA_WALLET_URL= set up READONLY access
```
