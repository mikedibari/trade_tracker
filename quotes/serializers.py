from rest_framework import serializers
from .models import Stock

class StockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stock
        fields = ('id', 'url', 'ticker', 'buy_price', 'quantity', 'sell_price', 'open_date', 'close_date')