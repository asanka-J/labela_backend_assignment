from .models import CartItem
from .serializers import CartItemSerializer

def format_cart_data(cart_data):
    cart_id = cart_data.get('id')
    cart_items = CartItem.objects.filter(cart=cart_id)
    cart_items_serializer = CartItemSerializer(cart_items, many=True)
    data = cart_data
    data['cart_items'] = cart_items_serializer.data
    return data
