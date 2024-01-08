from .models import CartItem
from .serializers import CartItemSerializer
from .models import OrderItem
from .serializers import OrderItemSerializer

def format_cart_data(cart_data):
    cart_id = cart_data.get('id')
    cart_items = CartItem.objects.filter(cart=cart_id)
    cart_items_serializer = CartItemSerializer(cart_items, many=True)
    data = cart_data
    data['cart_items'] = cart_items_serializer.data
    return data

def format_order_data(order_data):
    order_id = order_data.get('id')
    order_items = OrderItem.objects.filter(order=order_id)
    order_items_serializer = OrderItemSerializer(order_items, many=True)
    data = order_data
    data['order_items'] = order_items_serializer.data
    return data
