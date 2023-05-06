from django import forms
from .models import Stock


class StockForm(forms.ModelForm):
    ticker = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter ticker"}))
    buy_price = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "buy price"}))
    quantity = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "quantity"}))
    sell_price = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "sell price"}))
    open_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    close_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))


    class Meta:
        model = Stock
        fields = ['ticker', 'buy_price', 'quantity', 'sell_price', 'open_date', 'close_date']
        

    
