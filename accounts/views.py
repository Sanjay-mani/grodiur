# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from functools import wraps
from .models import UserProfile
import json

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        from .forms import RegisterForm
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, f"Welcome to Grodiur, {user.first_name}! 🎉")
            return redirect('home')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        from .forms import RegisterForm
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        from .forms import LoginForm
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}! 🛒")
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, "Invalid username or password.")
    else:
        from .forms import LoginForm
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'login_required': True, 'message': 'Please login to continue.'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@custom_login_required
def profile_view(request):
    total_orders = request.user.orders.count()
    completed_orders = request.user.orders.filter(status='delivered').count()
    return render(request, 'accounts/profile.html', {
        'total_orders': total_orders,
        'completed_orders': completed_orders
    })

@custom_login_required
def saved_addresses(request):
    from .models import Address
    addresses = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            if action == 'add':
                Address.objects.create(user=request.user, **{k:v for k,v in data.items() if k not in ['action', 'id']})
                return JsonResponse({'success': True})
            elif action == 'edit':
                Address.objects.filter(id=data.get('id'), user=request.user).update(**{k:v for k,v in data.items() if k not in ['action', 'id']})
                return JsonResponse({'success': True})
            elif action == 'delete':
                Address.objects.filter(id=data.get('id'), user=request.user).delete()
                return JsonResponse({'success': True})
            elif action == 'set_default':
                Address.objects.filter(user=request.user).update(is_default=False)
                Address.objects.filter(id=data.get('id'), user=request.user).update(is_default=True)
                return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return render(request, 'accounts/saved_addresses.html', {'addresses': addresses})

@custom_login_required
def payment_methods(request):
    return render(request, 'accounts/payment_methods.html')

@custom_login_required
def wishlist(request):
    from products.models import Wishlist
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'accounts/wishlist.html', {'items': items})

@custom_login_required
def add_to_wishlist(request, product_id):
    from products.models import Product, Wishlist
    product = get_object_or_404(Product, id=product_id)
    _, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created: messages.success(request, f"Added {product.name} to wishlist.")
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))

@custom_login_required
def remove_from_wishlist(request, product_id):
    from products.models import Wishlist
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    messages.success(request, "Removed from wishlist.")
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))

@custom_login_required
def settings_view(request):
    return render(request, 'accounts/settings.html')

@custom_login_required
def api_user_me(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return JsonResponse({
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'phone': profile.phone or '',
    })

@custom_login_required
def api_user_update(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        fname = data.get('firstName', '').strip()
        lname = data.get('lastName', '').strip()
        if not fname: return JsonResponse({'success': False, 'error': 'First name is required'}, status=400)
        request.user.first_name = fname
        request.user.last_name = lname
        request.user.save()
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return JsonResponse({
            'success': True,
            'user': {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone': profile.phone or '',
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)