from django.urls import path, include
from .views import (
    ProductViewSet, CartViewSet, CartItemViewSet, OrderViewSet
)


product_list = ProductViewSet.as_view({'get': 'list', 'post': 'create'})
product_detail = ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

cart_list = CartViewSet.as_view({'get': 'list'})
cart_get_or_create = CartViewSet.as_view({'get':'get'})

cart_item_create = CartItemViewSet.as_view({'get':'list','post': 'create'})
cart_item_delete = CartItemViewSet.as_view({'delete': 'destroy','put': 'update'})
cart_item_bulk_add = CartItemViewSet.as_view({'post': 'add_multiple_to_cart'})

order_view_set = OrderViewSet.as_view({'post': 'place_order','get':'list'})
order_detail = OrderViewSet.as_view({'get': 'get'})


urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    
    path('products', product_list, name='product-list'),
    path('products/<int:pk>', product_detail, name='product-detail'),
    
    path('cart', cart_get_or_create, name='cart-get-create'), 
    # path('cart/list/', cart_list, name='cart-list'), 
    
    path('cart/items', cart_item_create, name='cart-add'),
    path('cart/items/<int:pk>', cart_item_delete, name='cart-item-delete'),
    path('cart/items/bulk', cart_item_bulk_add, name='cart-item-bulk-add'),
    
    path('orders',order_view_set, name='order-place'),
    path('orders/<int:pk>', order_detail, name='order-detail'),
    
  
]


from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from django.urls import path


urlpatterns += [
    path("register", RegisterView.as_view(), name="rest_register"),
    path("login", LoginView.as_view(), name="rest_login"),
    path("logout", LogoutView.as_view(), name="rest_logout"),
    path("user", UserDetailsView.as_view(), name="rest_user_details"),
]