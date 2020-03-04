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

class CreateProduct(APIView):
    parser_classes = (FormParser, JSONParser, MultiPartParser)

    def post(self, request):
        serializer_class = Product2Serializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer_class.errors, status=status.HTTP_404_NOT_FOUND)

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
                "type" : str(actual_user.type),
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
            valPost = request.POST.get('user_id')

            try:
                comprobar_carrito = Cart.objects.get(pk=valPost)
                print "tiene carrito"

                product_id = request.POST.get('product_id')
                quantity = request.POST.get('quantity')
                product = Product2.objects.get(pk=product_id)
                total = product.price * int(quantity)
                purchase = ProductoCarrito(cart_id=valPost, product_id=product_id, total=total, quantity=quantity)
                purchase.save()
                data = {
                    "user_id": valPost,
                    "cart_id": comprobar_carrito.id,
                    "user_id": valPost,
                    "product_id": product_id,
                    "quantity": quantity,
                    "total": total,
                }
                return JsonResponse(data, safe=False)
            except ObjectDoesNotExist:
                print "Is in"

                cart = Cart(user_id=valPost, status_id=2)
                cart.save()
                print "carrito creado"


                product_id = request.POST.get('product_id')
                quantity = request.POST.get('quantity')
                product = Product2.objects.get(pk=product_id)
                total = product.price * int(quantity)
                purchase = ProductoCarrito(cart_id=valPost, product_id=product_id, total=total, quantity=quantity)
                purchase.save()
                data = {
                    "message": "carrito creado",
                    "user_id": valPost,
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
    VerPrpductoCarrito = ProductoCarrito.objects.all()
    if PurchaseCarts.count() > 0:
        for p in PurchaseCarts:
            for v in VerPrpductoCarrito:
                print p.pk
                data = {
                    "status": p.status.description,
                    "user_name": p.user.username,
                    "producto": v.product.name,
                }
                response_list.append(data)

        return JsonResponse(response_list, safe=False)
    else:
        return JsonResponse('error', safe=False)


@csrf_exempt
def getUserCart(request):
    print " Is in"
    response_list = []
    user_id = request.POST.get('user_id')
    user_id = request.POST.get('user_id')
    PurchaseCarts = ProductoCarrito.objects.filter(cart_id=user_id)
    if PurchaseCarts.count() > 0:
        for p in PurchaseCarts:
                print p.pk
                data = {
                    "status": p.cart.status.description,
                    "user_name": p.cart.user.username,
                    "producto": p.product.name
                }
                response_list.append(data)

        return JsonResponse(response_list, safe=False)
    else:
        return JsonResponse('error', safe=False)


@csrf_exempt
def BuyCart(request):
    if request.method == "POST":
        valPost = request.POST.get('user_id')
        comprobar_carrito = Cart.objects.get(pk=valPost)
        comprobar_carrito.status_id = 1
        comprobar_carrito.save()
        print comprobar_carrito.status.description








