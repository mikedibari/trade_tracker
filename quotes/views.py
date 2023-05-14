from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import Stock
from .models import Quote
from .serializers import StockSerializer
from .forms import StockForm
from django.contrib import messages
from django.conf import settings


# rest api for items in stock database model
class StockView(viewsets.ModelViewSet):
    queryset = Stock.objects.all().order_by('open_date')
    serializer_class = StockSerializer


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
        return round(profit_loss_dollars, 2)
    except TypeError:
        return None
    

def get_profit_loss_percent(current_value, cost_basis):
    try:
        profit_loss_percent = current_value / cost_basis - 1
        return round(profit_loss_percent, 2)
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

    return round(current_value, 2)


def get_cost_basis(buy_price, quantity):
    try:
        cost_basis = buy_price * quantity
        return round(cost_basis, 2)
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


def home(request): # request from web browser
    # import requests
    # import json

    # api_key = settings.API_KEY

    if request.method == 'POST': # someone filled out form and clicked the button
        ticker = request.POST['ticker'] # name of input box

        # api_url = "https://api.iex.cloud/v1/data/core/quote/" + ticker + "?token=" + api_key
        # api_request = requests.get(api_url)
    
        try:
            api = get_api(ticker)
            for item in api:
                instance = Quote(ticker=item['symbol'], company_name=item['companyName'])
                instance.save()

        except Exception as e:
            api = "Error..."        
           
        return render(request, 'home.html', {'api': api})

    else: # sends 'ticker' instead of 'api' to home
        return render(request, 'home.html', {'ticker': "Enter a ticker symbol above..."})
    

def quotes_table(request):
    quotes = Quote.objects.all().order_by('-id')
    combined_data = []
        
    for item in quotes:
        # get value for ticker column
        ticker = item.ticker
        quote_id = item.id 
        company_name = item.company_name        
        
        price_key = 'latestPrice'
        time_key = 'latestUpdate'
        change_key = 'change'
        change_percent_key = 'changePercent'

        latest_price = get_latest(ticker, price_key)
        time_in_seconds = get_latest(ticker, time_key)        
        latest_time = get_timestamp(time_in_seconds)
        change = get_latest(ticker, change_key)
        change_percent = get_latest(ticker, change_percent_key)

        # combine the data from the database and api
        combined_data.append({
            'ticker': ticker,
            'quote_id': quote_id,
            'company_name': company_name,            
            'latest_price': latest_price,
            'latest_time': latest_time,
            'change': change,
            "change_percent": change_percent            
        })
        
    return render(request, 'quotes.html', {'quotes': combined_data})
    

def about(request):
    return render(request, 'about.html', {})


def positions(request):    
    if request.method == 'POST': 
        # use django form system -- forms.py added
        form = StockForm(request.POST or None)
        ticker = form['ticker'].value()

        if form.is_valid() and check_ticker(ticker):
            form.save()
            messages.success(request, ("Position has been added!"))
            return redirect('positions')
        else:
            messages.success(request, ("Something went wrong..."))
            return redirect('positions')
    else:
        form = StockForm()
        # pull stuff from database model and call function for latest price
        data_from_database = Stock.objects.all().order_by('-id')
        combined_data = []
        
        for item in data_from_database:
            # get value for ticker column
            ticker = item.ticker
            stock_id = item.id
            buy_price = item.buy_price
            sell_price = item.sell_price
            quantity = item.quantity
            open_date = item.open_date
            close_date = item.close_date
            
            key = 'latestPrice'
            latest_price = get_latest(ticker, key)
            current_value = get_current_value(sell_price, latest_price, quantity)
            cost_basis = get_cost_basis(buy_price, quantity)            
            profit_loss_dollars = get_profit_loss_dollars(current_value, cost_basis)
            profit_loss_percent = get_profit_loss_percent(current_value, cost_basis)
            
            # combine the data from the database and api
            combined_data.append({
                'ticker': ticker,
                'latest_price': latest_price,
                'stock_id': stock_id,
                'buy_price': buy_price,
                'sell_price': sell_price,
                'quantity': quantity,
                'cost_basis': cost_basis,
                'current_value': current_value,
                'profit_loss_dollars': profit_loss_dollars,
                'profit_loss_percent': profit_loss_percent,
                'open_date': open_date,
                'close_date': close_date
            })

        return render(request, 'positions.html', {'form': form, 'data': combined_data})
    

def delete_row(request, stock_id):
    if request.method == 'POST':
        try:
            instance = Stock.objects.get(pk=stock_id)
            instance.delete()
            messages.success(request, ("Position has been deleted!"))
        except Stock.DoesNotExist:
            messages.error(request, ("Position does not exist."))        
    return redirect('positions')
    

def delete_quote(request, quote_id):
    if request.method == 'POST':
        # quote_id = request.POST.get('quote_id')
        try:
            instance = Quote.objects.get(pk=quote_id)
            instance.delete()
            messages.success(request, "Quote has been removed from the watchlist!")
        except Quote.DoesNotExist:
            messages.error(request, "Quote does not exist.") # test if this is needed
    return redirect('quotes')


# populates form fields with data from database
def update_position(request, stock_id):
    try:
        position = Stock.objects.get(pk=stock_id)    
        form = StockForm(instance=position)
    except Stock.DoesNotExist:
        messages.error(request, "Position does not exist.")
        return redirect('positions')
    return render(request, 'update_position.html', {'position': position, 'form': form})


# saves the edited fields to the correspoding database entry
def save_position(request):    
    if request.method == 'POST':
        stock_id = request.POST.get('stock_id') 
        position = Stock.objects.get(pk=stock_id)     
        form = StockForm(request.POST or None, instance=position)
        ticker = form['ticker'].value()
        if form.is_valid() and check_ticker(ticker):
            form.save()
            messages.success(request, ("Position has been updated!"))
            return redirect('positions')
        else:
            messages.success(request, ("Something went wrong..."))
            return redirect('positions')
    else:
        return redirect('positions')