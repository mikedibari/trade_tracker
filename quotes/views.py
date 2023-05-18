from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import Stock
from .models import Quote
from .serializers import StockSerializer
from .forms import StockForm
from django.contrib import messages
from .utils import *


# rest api
class StockView(viewsets.ModelViewSet):
    queryset = Stock.objects.all().order_by('open_date')
    serializer_class = StockSerializer


def home(request): # request from web browser
    if request.method == 'POST': # someone filled out form and clicked the button
        ticker = request.POST['ticker'] # name of input box in the form
        
        try:
            api = get_api(ticker)
            change_percent_key = 'changePercent'
            change_percent = get_latest(ticker, change_percent_key) * 100
            api_ohlc = get_api_ohlc(ticker)
            data = json_to_dataframe(api_ohlc)            
            chart = create_candlestick_chart(data, ticker)
            png_chart = fig_to_base64(chart)                                 

        except Exception as e:
            # print(e)
            api = "Error..." 
            change_percent = None            
            png_chart = None
        return render(request, 'home.html', {'api': api, 'change_percent': change_percent, 'png_chart': png_chart})

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
        change_percent = get_latest(ticker, change_percent_key) * 100

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
        stock_id = request.POST.get('stock_id') # form input hidden name
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
    
    
# add quote from home to watchlist unless already in database
def add_quote(request):
    if request.method == 'POST':
        ticker = request.POST.get('ticker')  # form input hidden name
        company_name = request.POST.get('company_name')
        try:
            Quote.objects.get(ticker=ticker)
            messages.error(request, "Quote is already in Watchlist.")
        except Quote.DoesNotExist:
            instance = Quote(ticker=ticker, company_name=company_name)
            instance.save()
            messages.success(request, "Quote has been added to Watchlist!")
    return redirect('quotes')

