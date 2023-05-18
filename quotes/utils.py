from django.conf import settings


# converts seconds since unix epoch to standard date and time
def get_timestamp(api_time):
    import datetime

    try:
        timestamp = api_time / 1000  # convert milliseconds to seconds
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt
    except TypeError:
        return None


def get_profit_loss_dollars(current_value, cost_basis):
    try:
        profit_loss_dollars = current_value - cost_basis        
        return profit_loss_dollars
    except TypeError:
        return None
    

def get_profit_loss_percent(current_value, cost_basis):
    try:
        profit_loss_percent = (current_value / cost_basis - 1) * 100
        return profit_loss_percent
    except TypeError:
        return None
    

# sell price or current price * quantity -- test this
def get_current_value(sell_price, latest_price, quantity):
    try:
        current_value = sell_price * quantity
    except TypeError:
        try:
            current_value = latest_price * quantity
        except TypeError:
            current_value = None
            return current_value

    return current_value


def get_cost_basis(buy_price, quantity):
    try:
        cost_basis = buy_price * quantity
        return cost_basis
    except TypeError:
        return None
    

def get_api(ticker):
    import requests
    import json

    api_key = settings.API_KEY
    
    try:
        response = requests.get("https://api.iex.cloud/v1/data/core/quote/" + ticker + "?token=" + api_key)        
        data_from_api = json.loads(response.content)
        return data_from_api        

    except Exception as e:
        print("An error occurred:", str(e))
        return []
    

def check_ticker(ticker):
    
    data_from_api = get_api(ticker)

    if isinstance(data_from_api, list) and len(data_from_api) > 0:
        # check if the ticker exists in the api response
        for item in data_from_api:
            if item is not None and item.get('symbol') == ticker.upper():
                return True

    return False
    
# get the latest from the api of any field passed in
def get_latest(ticker, key):
    
    data_from_api = get_api(ticker)
    
    if isinstance(data_from_api, list) and len(data_from_api) > 0:
        api_data_item = data_from_api[0]
        latest = api_data_item.get("" + key + "")
    else:
        latest = None        
    
    return latest


# api url that returns historical data
def get_api_ohlc(ticker):
    import requests
    import json

    api_key = settings.API_KEY
    date_range = '3m'
    
    try:
        response = requests.get("https://api.iex.cloud/v1/data/core/historical_prices/" + ticker + "?range=" + date_range + "&token=" + api_key)        
        data_from_api = json.loads(response.content)
        return data_from_api        

    except Exception as e:
        print("An error occurred:", str(e))
        return []
    

# convert json response from api to pandas df
def json_to_dataframe(json_data):
    import pandas as pd    

    rows = []
    for row in json_data:
        date = get_timestamp(row["date"])
        open_val = row["open"]
        high_val = row["high"]
        low_val = row["low"]
        close_val = row["close"]
        rows.append([date, open_val, high_val, low_val, close_val])
    df = pd.DataFrame(rows, columns=["date", "open", "high", "low", "close"])
    return df


# create chart from df using matplotlib
def create_candlestick_chart(df, ticker):    
    import matplotlib
    matplotlib.use('Agg') # prevents starting matplotlib gui outside main thread warning
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from mplfinance.original_flavor import candlestick_ohlc
    
    # convert date to a numerical representation that can be plotted on the x-axis    
    df['date'] = df['date'].apply(mdates.date2num)
    # print(df)

    fig, ax = plt.subplots()
    candlestick_ohlc(ax, df[['date', 'open', 'high', 'low', 'close']].values, width=0.6, 
                     colorup='green', colordown='red', alpha=1.0)    
    
    # allow grid
    ax.grid(True)

    # set labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    fig.suptitle(ticker.upper())

    # format Date
    date_format = mdates.DateFormatter('%d-%b')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()

    fig.tight_layout()
    return fig


# convert chart to png image
def fig_to_base64(fig):
    import io
    import base64

    img_bytes = io.BytesIO()
    fig.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    return base64.b64encode(img_bytes.read()).decode('ascii')
