from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import yfinance as yf
import ccxt
import os
import pandas_datareader.data as web

def get_forex_data_fred(symbol, start, end):
    data = web.get_data_fred(symbol, start, end)
    
    # Rename the 'VALUE' column to 'Close' for consistency
    if 'VALUE' in data.columns:
        data = data.rename(columns={'VALUE': 'Close'})

    return data


def get_forex_data(symbol, interval, start, end):
    exchange = ccxt.oandav20({
        'api_key': 'YOUR_API_KEY',
    })

    timeframe = map_interval_to_timeframe(interval)
    since = exchange.parse8601(f"{start}T00:00:00Z")
    to = exchange.parse8601(f"{end}T23:59:59Z")

    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, to)
    data = pd.DataFrame(ohlcv, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='ms')

    return data.set_index('Timestamp')

# import matplotlib.pyplot as plt

app = Flask(__name__)

# Add the existing functions (get_stock_data, calculate_sma, sma_crossover_strategy, calculate_profitability) here
def get_stock_data(ticker, interval, start, end):
    stock_data = yf.download(ticker, start=start, end=end, interval=interval)
    return stock_data

def calculate_sma(data, period, price_column='Close'):
    return data[price_column].rolling(window=period).mean()

def sma_crossover_strategy(data, sma_short, sma_long):
    signal = 0
    position = None
    buy_signals = []
    sell_signals = []
    
    for i in range(len(data)):
        if sma_short[i] > sma_long[i] and signal != 1:
            signal = 1
            position = data['Close'][i]
            buy_signals.append(data.index[i])
        elif sma_short[i] < sma_long[i] and signal != -1:
            signal = -1
            position = None
            sell_signals.append(data.index[i])

    return buy_signals, sell_signals

def sma_crossover_strategy(data, sma_short, sma_long):
    signal = 0
    position = None
    trades = []

    for i in range(len(data)):
        if sma_short[i] > sma_long[i] and signal != 1:
            signal = 1
            position = data.index[i]
        elif sma_short[i] < sma_long[i] and signal != -1 and position is not None:
            signal = -1
            sell_timestamp = data.index[i]
            trades.append((position, sell_timestamp))
            position = None

    return trades

def calculate_profitability(trades):
    returns = [(sell_price / buy_price - 1) for buy_price, sell_price in trades]
    overall_return = np.prod([1 + r for r in returns]) - 1
    return overall_return * 100

@app.route('/data', methods=['GET'])
def get_data():
    symbol = request.args.get('symbol')
    interval = request.args.get('interval')
    start = request.args.get('start')
    end = request.args.get('end')

    is_forex = '/' in symbol
    is_fred_forex = symbol.startswith('DEX')

    if is_forex and not is_fred_forex:
        data = get_forex_data(symbol, interval, start, end)
    elif is_fred_forex:
        data = get_forex_data_fred(symbol, start, end)
    else:
        data = get_stock_data(symbol, interval, start, end)

    data.reset_index(inplace=True)
    data_dict = data.to_dict(orient='records')

    return jsonify(data_dict)

@app.route('/backtest', methods=['GET'])
def backtest():
    strategy = request.args.get('strategy')
    symbol = request.args.get('symbol')
    interval = request.args.get('interval')
    start = request.args.get('start')
    end = request.args.get('end')
    sma_short_period = int(request.args.get('sma_short_period'))
    sma_long_period = int(request.args.get('sma_long_period'))

    is_forex = '/' in symbol
    is_fred_forex = symbol.startswith('DEX')
    market = "stocks"
    if is_forex and not is_fred_forex:
        data = get_forex_data(symbol, interval, start, end)
        market == "forex"
    elif is_fred_forex:
        data = get_forex_data_fred(symbol, start, end)
        market == "forex"
    else:
        data = get_stock_data(symbol, interval, start, end)

    if strategy == 'sma_crossover':
        if market == "forex":
            price_column = "PRICE"
        else:
            price_column = "Close"

        data['sma_short'] = calculate_sma(data, sma_short_period, price_column)
        data['sma_long'] = calculate_sma(data, sma_long_period, price_column)
        trades = sma_crossover_strategy(data, data['sma_short'], data['sma_long'])
        profitability = calculate_profitability([(data['Close'][buy], data['Close'][sell]) for buy, sell in trades])

        response = {
            'profitability': round(profitability, 2),
            'trades': [
                {
                    'buy_timestamp': str(buy_timestamp),
                    'sell_timestamp': str(sell_timestamp),
                }
                for buy_timestamp, sell_timestamp in trades
            ],
        }

        return jsonify(response)
    else:
        return jsonify({'error': 'Invalid strategy'}), 400

@app.route('/')
def index():
    instructions = '''
    <h1>Welcome to the Stock and Forex Backtesting API!</h1>
    <p>Use one of the following routes to access the API functionalities:</p>
    <ul>
        <li>
            <b>Stock Backtesting:</b> /backtest?strategy=[strategy]&symbol=[symbol]&interval=[interval]&start=[start_date]&end=[end_date]&sma_short_period=[short_period]&sma_long_period=[long_period]
        </li>
        <li>
            <b>Forex Backtesting:</b> /backtest?market=forex&strategy=[strategy]&symbol=[symbol]&interval=[interval]&start=[start_date]&end=[end_date]&sma_short_period=[short_period]&sma_long_period=[long_period]
        </li>
    </ul>
    <p>Replace the values inside the square brackets with the appropriate values for each parameter.</p>
    '''
    return instructions

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
