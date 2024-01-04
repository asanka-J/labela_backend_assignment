from django.shortcuts import render
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Cart, CartItem, Order
from .serializers import ProductSerializer, CartSerializer, OrderSerializer, CartItemSerializer, OrderItemSerializer
from rest_framework.permissions import AllowAny

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
    def get(self, request, *args, **kwargs):
        cart_id = request.query_params.get('cart_id')
    
        if cart_id: # If cart_id is provided
            try:
                cart = Cart.objects.get(cart_id=cart_id)
                if cart.user:   # If the cart is associated with a user
                    if cart.user == request.user: # If the cart is associated with the user
                        serializer = self.get_serializer(cart)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                else:   # If the cart is not associated with a user
                    serializer = self.get_serializer(cart)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                    
                return Response({"message": "Unauthorized access to cart"}, status=status.HTTP_403_FORBIDDEN)
            except Cart.DoesNotExist:
                return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user.is_authenticated:
            existing_cart = Cart.objects.filter(user=request.user).first()
            if existing_cart:
                serializer = self.get_serializer(existing_cart)
                return Response(serializer.data, status=status.HTTP_200_OK)

            cart = Cart.objects.create(user=request.user)
            serializer = self.get_serializer(cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            cart = Cart.objects.create()
            serializer = self.get_serializer(cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
