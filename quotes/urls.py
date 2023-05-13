from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('positions', views.StockView)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.home, name="home"),
    path('quotes.html', views.quotes_table, name="quotes"),
    path('about.html', views.about, name="about"),
    path('positions.html', views.positions, name="positions"),
    path('delete_row/<int:stock_id>/', views.delete_row, name="delete_row"),
    path('delete_quote/<int:quote_id>/', views.delete_quote, name="delete_quote"),
    path('update_position/<int:stock_id>/', views.update_position, name="update_position"),
    path('save_position/', views.save_position, name="save_position"),
    
]