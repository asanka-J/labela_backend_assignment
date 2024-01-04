from django.shortcuts import render
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Product#, Cart, CartItem, Order
from .serializers import ProductSerializer#, CartSerializer, OrderSerializer, CartItemSerializer, OrderItemSerializer
from rest_framework.permissions import AllowAny

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

