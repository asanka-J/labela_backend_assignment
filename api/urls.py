from django.urls import path, include
from .views import (
    ProductViewSet, CartViewSet, CartItemViewSet
)


product_list = ProductViewSet.as_view({'get': 'list', 'post': 'create'})
product_detail = ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

cart_list = CartViewSet.as_view({'get': 'list'})
cart_create = CartViewSet.as_view({'get':'get','post': 'create'})

cart_item_create = CartItemViewSet.as_view({'get':'list','post': 'create'})
cart_item_delete = CartItemViewSet.as_view({'delete': 'destroy'})
cart_item_update = CartItemViewSet.as_view({'put': 'update'})
cart_item_bulk_add = CartItemViewSet.as_view({'post': 'add_multiple_to_cart'})

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    
    path('products/', product_list, name='product-list'),
    path('products/<int:pk>/', product_detail, name='product-detail'),
    
    path('cart/', cart_create, name='cart-create'), 
    path('cart/list/', cart_list, name='cart-list'),
    
    path('cart/item/add/', cart_item_create, name='cart-add'),
    path('cart/item/<item_id>/delete', cart_item_delete, name='cart-item-delete'),
    path('cart/item/bulk', cart_item_bulk_add, name='cart-item-bulk-add'),

   
]
