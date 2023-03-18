---
title: Flask
description: A popular minimal server framework for Python
tags:
  - python
  - flask
---

# Python Flask Example

This is a [Flask](https://flask.palletsprojects.com/en/1.1.x/) app that serves a simple JSON response.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/zUcpux)

## ✨ Features

- Python
- Flask

## 💁‍♀️ How to use

- Install Python requirements `pip install -r requirements.txt`
- Start the server for development `python3 main.py`

## Endpoints

### /data

Returns historical stock or forex data.

#### Example curl queries

##### Stock

    curl 'http://127.0.0.1:5000/data?symbol=AAPL&interval=1d&start=2023-02-01&end=2023-03-01'

    curl 'https://flask-production-930b.up.railway.app/data?symbol=AAPL&interval=1d&start=2023-02-01&end=2023-03-01'

##### Forex (FRED)

    curl 'http://127.0.0.1:5000/data?symbol=DEXUSEU&interval=1d&start=2023-02-01&end=2023-03-01'

    curl 'https://flask-production-930b.up.railway.app/data?symbol=DEXUSEU&interval=1d&start=2023-02-01&end=2023-03-01'

### /backtest

Backtests a simple moving average crossover trading strategy on the given stock or forex data.

#### Example curl queries

##### Stock

    curl 'http://127.0.0.1:5000/backtest?strategy=sma_crossover&symbol=MSFT&interval=1d&start=2021-01-01&end=2021-12-31&sma_short_period=10&sma_long_period=30'

    curl 'https://flask-production-930b.up.railway.app/backtest?strategy=sma_crossover&symbol=MSFT&interval=1d&start=2021-01-01&end=2021-12-31&sma_short_period=10&sma_long_period=30'

##### Forex (FRED)

    curl 'http://127.0.0.1:5000/backtest?strategy=sma_crossover&symbol=DEXUSEU&interval=1d&start=2023-02-01&end=2023-03-01&sma_short_period=50&sma_long_period=200'

    curl 'https://flask-production-930b.up.railway.app/backtest?strategy=sma_crossover&symbol=DEXUSEU&interval=1d&start=2023-02-01&end=2023-03-01&sma_short_period=50&sma_long_period=200'


## Notes

1. FRED data is limited and only provides daily frequency for specific currency pairs. If you need more comprehensive forex data, you may need to use a data provider that requires an API key, such as Oanda or Alpha Vantage.


