from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from .serializer import *
from . import serializer
from .models import *
from rest_framework import generics
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.parsers import JSONParser,FormParser,MultiPartParser
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict
from django.http import JsonResponse, JsonResponse
from django.db.models import Exists
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Max, Min, Sum

class CreateProduct(APIView):
    parser_classes = (FormParser, JSONParser, MultiPartParser)

    def post(self, request):
        serializer_class = Product2Serializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer_class.errors, status=status.HTTP_404_NOT_FOUND)

class ProductList(generics.ListAPIView):
    queryset = Product2.objects.all()
    serializer_class = Product2Serializer

class UserCreate(generics.ListCreateAPIView):
    parser_classes = (FormParser, JSONParser,MultiPartParser)

    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        print [request.data]
        serializer_class = UserSerializer(data=request.data)
        print serializers
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    parser_classes = (FormParser, JSONParser, MultiPartParser)
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        actual_user = User.objects.get(username=username)

        if password==actual_user.password:
            print [request.data]
            response = {
                "message": 'success',
                "id": actual_user.id,

            }
            return Response(response,status=status.HTTP_200_OK)
        else:
            print ('no entro')
            response = {
                "message": 'error'
            }

            return Response(response, status=status.HTTP_403_FORBIDDEN)

@csrf_exempt
def AddCart(request):
    if request.method == "POST":
            user_id = request.POST.get('user_id')

            try:
                comprobar_carrito = Cart.objects.get(user_id=user_id)
                print "tiene carrito"
                product_id = request.POST.get('product_id')
                quantity = request.POST.get('quantity')
                product = Product2.objects.get(pk=product_id)
                total = product.price * int(quantity)
                purchase = ProductoCarrito(cart_id=user_id, product_id=product_id, total=total, quantity=quantity,
                                           status_id=2)
                purchase.save()
                data = {
                    "user_id": user_id,
                    "cart_id": comprobar_carrito.id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "total": total,
                }
                return JsonResponse(data, safe=False)


            except ObjectDoesNotExist:

                print "Is in"
                cart = Cart(user_id=user_id, status_id=2)
                cart.save()
                print "carrito creado"
                product_id = request.POST.get('product_id')
                quantity = request.POST.get('quantity')
                product = Product2.objects.get(pk=product_id)
                total = product.price * int(quantity)
                purchase = ProductoCarrito(cart_id=user_id, product_id=product_id, total=total, quantity=quantity,
                                           status_id=2)

                purchase.save()
                data = {

                    "message": "carrito creado",
                    "user_id": user_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "total": total,
                    # "cart_id": comprobar_carrito
                }

                return JsonResponse(data, safe=False)

def GetAllCart (request):
    print " Is in"
    response_list = []
    # user_id = request.POST.get('user_id')
    PurchaseCarts = Cart.objects.all()

    #return JsonResponse(data,safe=False)

class getAllCart(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

@csrf_exempt
def getUserCart(request):
    print " Is in"
    response_list = []
    user_id = request.POST.get('user_id')
    print user_id
    cart = Cart.objects.get(user_id=user_id)
    value = ProductoCarrito.objects.filter(cart_id=user_id)
    print value
    if value.count() > 0:
        for p in value:
                print p.cart_id
                print "staus compra",p.status.description
                data = {
                    "user": cart.user.username,
                    "status": cart.status.description,
                    "producto": p.product.name,
                    "quantity": p.quantity,
                    "stock": p.product.stock
                }
                response_list.append(data)

        return JsonResponse(response_list, safe=False)
    else:
        return JsonResponse('error sin productos', safe=False)


@csrf_exempt
def BuyCart(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        cart_status = Cart.objects.get(user_id=user_id)
        value = ProductoCarrito.objects.get(cart_id=user_id)
        cart_status.status.id = 1
        #comprobar_producto.status_id = 2
        cart_status.save()
        #comprobar_producto.save()

        PurchaseCarts = ProductoCarrito.objects.filter(cart_id=user_id)
        for p in PurchaseCarts:
            if p.product.stock < 0:
               total_stock = p.product.stock - p.quantity
               p.product.stock = total_stock
               p.product.save()

               print "total:" + str(total_stock)
            data = {
                "status": cart_status.status.description,
                "cart_id":  cart_status.id,
                "username": cart_status.user.username
                    }
            return JsonResponse(data,safe=False)

@csrf_exempt
def computeTicketValue(request):
    if request.method == 'POST':

        usario_carrito = request.POST.get('user_id')
        #carrito_products = request.POST.get('cart_id')  # el string es como lo manda en el reques
        cart = Cart.objects.get(user_id=usario_carrito)
        if cart.status.description == 'comprado':
            print "Is in"
            obj_producto = ProductoCarrito.objects.filter(cart_id=usario_carrito)
            print obj_producto
            ticket = obj_producto.all().aggregate(Sum('total'))
            print ticket
            data = {
                "cart_id": cart.id,
                "username": cart.user.username,
                "total": ticket,
            }
            return JsonResponse(data, safe=False)
        else:
            print cart.status.description
            return JsonResponse('necesitas comprar el carro', safe=False)



@csrf_exempt
def DeleteCart(request):
    if request.method == 'POST':
        usario_carrito = request.POST.get('user_id')
        cart = Cart.objects.get(user_id=usario_carrito)
        cart.status_id = 3
        cart.save()

        data = {
            "status": cart.status.description,
            "cart_id": cart.id,
            "username": cart.user.username
        }
        return JsonResponse(data,safe=False)










