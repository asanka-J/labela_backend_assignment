from django.urls import path, include
from .views import (
    ProductViewSet,CartViewSet
)


product_list = ProductViewSet.as_view({'get': 'list', 'post': 'create'})
product_detail = ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
cart_list = CartViewSet.as_view({'get': 'list'})
cart_create = CartViewSet.as_view({'get':'get','post': 'create'})

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    
    path('products/', product_list, name='product-list'),
    path('products/<int:pk>/', product_detail, name='product-detail'),
    
    path('cart/', cart_create, name='cart-create'), 
    path('cart/list/', cart_list, name='cart-list'),

   
]
