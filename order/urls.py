from django.urls import path
from .views import OrderViewSet

order_view_set = OrderViewSet.as_view({'post': 'place_order','get':'list'})
order_detail = OrderViewSet.as_view({'get': 'get'})

urlpatterns = [

    path('',order_view_set, name='order-place'),
    path('<int:pk>', order_detail, name='order-detail'),
    
]