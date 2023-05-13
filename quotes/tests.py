from django.test import TestCase
import pytest
from django.urls import reverse
from django.test import Client
from quotes.forms import StockForm
from datetime import datetime
from quotes.models import Stock
from quotes.models import Quote


# create dummy web browser
@pytest.fixture
def client():
    client = Client()
    return client


# get the home page url
def test_homepage_access(client):
    url = reverse('home')
    response = client.get(url)    
    assert response.status_code == 200


# verify that the form is valid and page redirects back to itself 
@pytest.mark.django_db
def test_positions_view(client):
    url = reverse('positions')
    form_data = {
        'ticker': 'AAPL',
        'buy_price': 100,
        'sell_price': 120,
        'quantity': 10,
        'open_date': '2022-01-01',
        'close_date': '2022-01-02',
    }
    form = StockForm(data=form_data)
    assert form.is_valid()

    response = client.post(url, data=form_data)
    assert response.status_code == 302 # redirect status code

    # verify that stock was added to the database
    stock = Stock.objects.last()
    assert stock.ticker == 'AAPL'
    assert stock.buy_price == 100
    assert stock.sell_price == 120
    assert stock.quantity == 10
    assert stock.open_date == datetime.strptime('2022-01-01', '%Y-%m-%d').date()
    assert stock.close_date == datetime.strptime('2022-01-02', '%Y-%m-%d').date()


# verify that data added to the db shows up on the page
@pytest.mark.django_db
def test_quotes_table(client):
    # create some test data
    Quote.objects.create(ticker='AAPL', company_name='Apple Inc.')
    Quote.objects.create(ticker='GOOGL', company_name='Alphabet Inc.')

    # get quotes page url
    url = reverse('quotes')
    response = client.get(url)    
    assert response.status_code == 200

    # ensure the response contains the expected data
    assert b'AAPL' in response.content
    assert b'Apple Inc.' in response.content
    assert b'GOOGL' in response.content
    assert b'Alphabet Inc.' in response.content
