from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.shortcuts import render


from products import views as product_views


def home_view(request):
    from products.models import Category
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('product/<int:product_id>/', product_views.product_detail_by_id, name='product_detail_by_id'),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('reviews/', include('reviews.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('api/products/<int:product_id>/reviews/', product_views.product_reviews_api, name='product_reviews_api_direct'),
    path('api/', include('otp_auth.urls')),
    
    path('accounts/', include('allauth.urls')),

    path('', home_view, name='home'),
]

# Serve media files regardless of DEBUG status
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
