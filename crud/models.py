# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50, blank=False)


    def __unicode__(self):
        return '{}'.format(self.username)



class Product2(models.Model):
    name = models.CharField(max_length=70)
    stock = models.IntegerField(blank=True)
    price = models.IntegerField(blank=True)

    def __unicode__(self):
        return unicode(self.name)


class StatusCarrito(models.Model):
    description = models.CharField(max_length= 30,default=True, blank=True)



class Cart(models.Model):
    user = models.ForeignKey(User, unique=False)
    date = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(StatusCarrito, default=True)

    def __unicode__(self):
        return unicode(self.user)


class ProductoCarrito(models.Model):
    cart = models.ForeignKey(Cart)
    product = models.ForeignKey(Product2)
    total = models.FloatField()
    quantity = models.IntegerField()
    status = models.ForeignKey(StatusCarrito, default=True)


    def __unicode__(self):
        return unicode(self.product)