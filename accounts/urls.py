# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('saved-addresses/', views.saved_addresses, name='saved_addresses'),
    path('payment-methods/', views.payment_methods, name='payment_methods'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('settings/', views.settings_view, name='settings'),
    
    # API
    path('api/user/me', views.api_user_me, name='api_user_me'),
    path('api/user/update', views.api_user_update, name='api_user_update'),
    path('update-name/', views.api_user_update, name='update_name'),
]