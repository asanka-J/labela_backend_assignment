
from django.urls import path
from .views import CartViewSet, CartItemViewSet

cart_list = CartViewSet.as_view({'get': 'list'})
cart_get_or_create = CartViewSet.as_view({'get':'get'})

cart_item_create = CartItemViewSet.as_view({'get':'list','post': 'create'})
cart_item_delete = CartItemViewSet.as_view({'delete': 'destroy','put': 'update'})
cart_item_bulk_add = CartItemViewSet.as_view({'post': 'add_multiple_to_cart'})


urlpatterns = [
    
    path('', cart_get_or_create, name='cart-get-create'), 
    # path('cart/list/', cart_list, name='cart-list'), 
    
    path('items', cart_item_create, name='cart-add'),
    path('items/<int:pk>', cart_item_delete, name='cart-item-delete'),
    path('items/bulk', cart_item_bulk_add, name='cart-item-bulk-add'),
    
]