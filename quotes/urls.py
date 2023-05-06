from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('stocks', views.StockView)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.home, name="home"),
    path('quotes.html', views.quotes_table, name="quotes"),
    path('about.html', views.about, name="about"),
    path('add_stock.html', views.add_stock, name="add_stock"),
    path('delete_row/<int:stock_id>/', views.delete_row, name="delete_row"),
    path('delete_quote/', views.delete_quote, name="delete_quote"),
    
]