from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:item_id>/', views.update_cart_ajax, name='update_cart_ajax'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('api/coupon/apply', views.apply_coupon, name='api_apply_coupon'),
    path('remove-coupon/', views.remove_coupon, name='remove_coupon'),
    path('api/cart-count/', views.get_cart_count, name='api_cart_count'),
    path('api/json/', views.api_cart_json, name='api_cart_json'),
]