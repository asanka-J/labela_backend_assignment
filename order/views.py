from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from cart.models import Cart, CartItem
from order.models import Order, OrderItem
from .serializers import OrderSerializer
from django.db import transaction

from autocompany.utils import format_order_data
   
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

        
    def get(self, request, pk=None):
        response_data = {}

        try:
            order = Order.objects.get(id=pk)
            serializer = self.get_serializer(order)
            response_data["message"] = "Order found"
            response_data["order"] = format_order_data(serializer.data)
            return Response(response_data, status=status.HTTP_200_OK)
                
        except Order.DoesNotExist:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
             