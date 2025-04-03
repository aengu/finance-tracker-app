from django.urls import path
from tracker import views


urlpatterns = [
    path("", views.index, name='index'),
    path("transactions_list", views.transaction_list, name='transaction_list'),
]
