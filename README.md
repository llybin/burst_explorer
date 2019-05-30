# BurstCoin Blockchain Explorer

[![Build Status](https://travis-ci.com/llybin/burst_explorer.svg?branch=master)](https://travis-ci.com/llybin/burst_explorer)
[![GPLv3](https://img.shields.io/badge/license-GPLv3-blue.svg)](LICENSE)

## Donations

**BURST-D372-C2DU-HMKK-CQLHA** or [**Paypal**](https://paypal.me/lybin) 

You can test it [here](http://explorer.burst.devtrue.net/)

Explorer and Burst node аre running on one **$5/mo 1GB 1CPU 25GB SSD Disk**

Sign up using my link and [receive $100](https://www.digitalocean.com/?refcode=ba04a478e10d)

## How to run

See additional info about set up DB [here](java_wallet)

### Development

`docker-compose up`

### Production

`cp .env.default .env`

Configure your .env:

``` console
DEBUG=False
SECRET_KEY= set up
DB_DEFAULT_URL= set up
DB_JAVA_WALLET_URL= set up
```

### Docker

_TODO_

### Without docker

Python >=3.6

`# apt install python3 python3-pip`

`# apt install libmysqlclient-dev`

`pip3 install --user pipenv`

``` console
export PATH="/home/<user>/.local/bin:$PATH"
echo 'export PATH="/home/<user>/.local/bin:$PATH"' >> ~/.bashrc
```

`pipenv install`

`pipenv run ./manage.py runserver 0.0.0.0:80`

_TODO: wsgi_
