from django.shortcuts import render
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Cart, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CartSerializer, OrderSerializer, CartItemSerializer, OrderItemSerializer
from rest_framework.permissions import AllowAny
from django.db import transaction

from rest_framework.pagination import PageNumberPagination
from .utils import format_cart_data

class CustomPagination(PageNumberPagination):
    page_size = 5 
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
            
    def get(self, request, *args, **kwargs):
        cart_id = request.query_params.get('cart_id')
        response_data = {}

        if cart_id: # If cart_id is provided
            try:
                cart = Cart.objects.get(cart_id=cart_id)
                if cart.user:   # If the cart is associated with a user
                    if cart.user == request.user: # If the cart is associated with the user
                        serializer = self.get_serializer(cart)
                        response_data["message"] = "Cart found"
                        response_data["cart"] = format_cart_data(serializer.data)
                        return Response(response_data, status=status.HTTP_200_OK)
                else:   # If the cart is not associated with a user
                    serializer = self.get_serializer(cart)
                    response_data["message"] = "Guest cart found"
                    response_data["cart"] = format_cart_data(serializer.data)
                    return Response(response_data, status=status.HTTP_200_OK)
                    
                return Response({"message": "Unauthorized access to cart"}, status=status.HTTP_403_FORBIDDEN)
            except Cart.DoesNotExist:
                return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user.is_authenticated:
            existing_cart = Cart.objects.filter(user=request.user).first()
            if existing_cart:
                serializer = self.get_serializer(existing_cart)
                response_data["message"] = "Cart already exists"
                response_data["cart"] = format_cart_data(serializer.data)
                return Response(response_data, status=status.HTTP_200_OK)

            cart = Cart.objects.create(user=request.user)
            serializer = self.get_serializer(cart)
            response_data["message"] = "Cart created successfully"
            response_data["cart"] = format_cart_data(serializer.data)
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            cart = Cart.objects.create()
            serializer = self.get_serializer(cart)
            response_data["message"] = "Cart created successfully"
            response_data["cart"] = format_cart_data(serializer.data)
            return Response(response_data, status=status.HTTP_201_CREATED)
        
class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
        
    def create(self, request):
        cart_id = request.data.get('cart_id')
        product_data = request.data.get('product') 
        response_data = {}

        if not product_data:
            return Response({"message": "Product data not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        product_id = product_data.get('id')
        quantity = product_data.get('quantity', 1) 

        if cart_id:
            try:
                cart = Cart.objects.get(cart_id=cart_id)
            except Cart.DoesNotExist:
                return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
    
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                cart_item = CartItem.objects.get(cart=cart, product=product)
                cart_item.quantity += quantity
            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(cart=cart, product=product,quantity=quantity)
            cart_item.save()

            cart_serializer = CartSerializer(cart)
            response_data["message"] = "Product added to the cart"
            response_data["cart"] = format_cart_data(cart_serializer.data)
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Cart ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        cart_id = request.data.get('cart_id')
        quantity = request.data.get('quantity')
        
        if cart_id:
            try:
                cart = Cart.objects.get(cart_id=cart_id)
                cart_item = CartItem.objects.get(pk=pk, cart=cart)
            except Cart.DoesNotExist:
                return Response({"message": "Invalid Cart id"}, status=status.HTTP_404_NOT_FOUND)
            except CartItem.DoesNotExist:
                return Response({"message": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)   
                     
            if quantity is not None:
                if quantity > 0:
                    cart_item.quantity = quantity
                    cart_item.save()
                elif quantity == 0:
                    cart_item.delete()
                else:
                    return Response({"message": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST) 
            else:
                return Response({"message": "Quantity not provided"}, status=status.HTTP_400_BAD_REQUEST)

            cart_serializer = CartSerializer(cart_item.cart)
            return Response(format_cart_data(cart_serializer.data), status=status.HTTP_200_OK)
        
    def destroy(self, request, pk=None):
        cart_id = request.data.get('cart_id')
        
        if cart_id:
            try:
                cart = Cart.objects.get(cart_id=cart_id)
                cart_item = CartItem.objects.get(pk=pk, cart=cart)
                cart_item.delete()
                return Response({"message": "Product removed"}, status=status.HTTP_204_NO_CONTENT)
            except Cart.DoesNotExist:
                return Response({"message": "Invalid Cart item id"}, status=status.HTTP_404_NOT_FOUND)
            except CartItem.DoesNotExist:
                return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message": "Cart ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    def add_multiple_to_cart(self, request): 
        cart_id = request.data.get('cart_id')
        items = request.data.get('items', [])  # Items should be a list of dictionaries containing product_id and quantity
        response_data= {}

        if not items: 
            return Response({"message": "No items provided"}, status=status.HTTP_400_BAD_REQUEST)

        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            cart = Cart.objects.create()

        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"message": f"Product with ID {product_id} not found"}, status=status.HTTP_404_NOT_FOUND)

            if quantity <= 0:
                return Response({"message": f"Invalid quantity provided for Product ID {product_id}"}, status=status.HTTP_400_BAD_REQUEST)

            cart_item = CartItem.objects.get(cart=cart, product=product)
            if cart_item:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
                cart_item.save()

        cart_serializer = CartSerializer(cart)
        response_data["message"] = "Product added to the cart"
        response_data["cart"] = format_cart_data(cart_serializer.data)
        return Response(response_data, status=status.HTTP_200_OK)

    
class OrderViewSet(ModelViewSet):
    
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    
    def place_order(self, request):
        cart_id = request.data.get('cart_id')
        delivery_date_time = request.data.get('delivery_date_time')
        name = request.data.get('name')
        address = request.data.get('address')
        email = request.data.get('email')
        
        try:
            cart = Cart.objects.get(cart_id=cart_id)
            cart_items = CartItem.objects.filter(cart=cart)
        except Cart.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic(): # Start a database transaction
            try:
                order = Order.objects.create(
                    user = request.user.id if request.user.is_authenticated else None,
                    delivery_date_time=delivery_date_time,
                    name=name,
                    address=address,
                    email =email
                )
                
                for cart_item in cart_items:
                    product = cart_item.product
                    quantity = cart_item.quantity
                    
                    if product.quantity < quantity:
                        raise Exception(f"Product {product.name} has insufficient quantity")
                    
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity
                    )
                    
                    product.quantity -= quantity
                    product.save()
                    
                    # Clear cart after successful order place
                    cart_items.delete()
                
                return Response({"message": "Order placed successfully"}, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                transaction.set_rollback(True)
                return Response({"message": f"Order placement failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
    
    @staticmethod
    def format_order_data(order_data):
        order_id = order_data.get('id')
        order_items = OrderItem.objects.filter(order=order_id)
        order_items_serializer = OrderItemSerializer(order_items, many=True)
        data = order_data
        data['order_items'] = order_items_serializer.data
        return data
        
        
    def get(self, request, pk=None):
        response_data = {}

        try:
            order = Order.objects.get(id=pk)
            serializer = self.get_serializer(order)
            response_data["message"] = "Order found"
            response_data["order"] = self.format_order_data(serializer.data)
            return Response(response_data, status=status.HTTP_200_OK)
                
        except Order.DoesNotExist:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
             