from django.urls import path, include
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from django.urls import path

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('products/', include('product.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('order.urls')),
    
]

# Rest auth urls
urlpatterns += [
    path("register", RegisterView.as_view(), name="rest_register"),
    path("login", LoginView.as_view(), name="rest_login"),
    path("logout", LogoutView.as_view(), name="rest_logout"),
    path("user", UserDetailsView.as_view(), name="rest_user_details"),
]