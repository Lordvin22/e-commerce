from django.conf.urls import url
from django.contrib import admin
from rest_framework import routers
from crud.viewsets import *


urlpatterns = [
    url(r'^v1/add_products/$', CreateProduct.as_view(), name='product_add'),
    url(r'^v1/get_products/$', ProductList.as_view(), name='product_list'),

    url(r'^v2/add_user/$', UserCreate.as_view(), name='user_create'),
    url(r'^v2/login/$', Login.as_view(), name='login'),

    #url(r'^v3/create_cart/$', createCart, name='createCart'),
    url(r'^v3/add_cart/$', AddCart, name='addCart'),
    url(r'^v3/buy_cart/$', BuyCart, name='buyCart'),
    url(r'^v3/get_usercart/$', getUserCart, name='getUserCart'),
    url(r'^v3/get_allcart/$', getAllCart.as_view(), name='getAllCart'),
    url(r'^v3/delete_cart/$', DeleteCart, name='getUserCart'),

    url(r'^v4/get_ticket/$', computeTicketValue, name='getTicket'),


]