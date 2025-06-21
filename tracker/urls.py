from django.urls import path
from tracker import views


urlpatterns = [
    path("", views.index, name='index'),
    path("transactions/", views.transaction_list, name='transaction-list'),
    path("transactions/create/", views.create_transaction, name='create-transaction'),
]
