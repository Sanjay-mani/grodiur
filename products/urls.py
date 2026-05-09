from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('api/categories/', views.get_categories, name='api_categories'),
    path('api/search/', views.api_product_search, name='api_product_search'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]