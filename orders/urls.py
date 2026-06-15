from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('success/<str:order_id>/', views.order_success, name='order_success'),
    path('history/', views.order_history, name='order_history'),
    path('again/<str:order_id>/', views.order_again, name='order_again'),
    path('<str:order_id>/invoice/', views.order_invoice, name='order_invoice'),
    path('<str:order_id>/support/', views.submit_support_ticket, name='submit_support_ticket'),

    
    # API
    path('api/orders', views.api_orders, name='api_orders'),
    path('api/recent-orders/', views.api_recent_orders, name='api_recent_orders'),
    path('api/orders/<str:order_id>', views.api_order_detail_json, name='api_order_detail_json'),
    
    path('api/create-razorpay-order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('razorpay-webhook/', views.razorpay_webhook, name='razorpay_webhook'),
    path('success/', views.latest_order_success, name='order_success_latest'),
    path('<str:order_id>/', views.order_detail, name='order_detail'),
]