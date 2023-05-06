from django.db import models


class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    buy_price = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    sell_price = models.FloatField(null=True, blank=True)
    open_date = models.DateField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.ticker
    
class Quote(models.Model):
    ticker = models.CharField(max_length=10) 
    company_name = models.CharField(max_length=100, null=True, blank=True)     
        
    def __str__(self):
        return self.ticker