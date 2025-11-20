from django.urls import path
from . import views

app_name = 'funds'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_funds/', views.add_funds, name='add_funds'),
    path('change_funds/<int:id>', views.change_funds, name='change_funds'),
    path('delete_funds/<int:id>', views.delete_funds, name='delete_funds'),
    path('transactions/', views.view_transactions, name='view_transactions'),
]