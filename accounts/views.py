# accounts/views.py
"""
GRODIUR - ACCOUNTS VIEW CONTROLLERS
==================================
This module serves as the primary controller logic (Views in MVT) for user identity, 
security states, profiles, addresses, and wishlist management.
It handles client HTTP requests, validates state (e.g., login requirements),
interacts with SQLite models via the Django ORM, and returns either HTML page responses 
or structured API JSON data.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from functools import wraps
from .models import UserProfile
import json


def register_view(request):
    """
    CUSTOMER REGISTRATION VIEW
    --------------------------
    - GET request: Renders a blank registration HTML form.
    - POST request: Validates user details and signs them up securely.
      - Upon successful validation, it automatically creates a corresponding
        UserProfile object and signs the user in instantly, transitioning them to 'home'.
    """
    # If the user is already signed in, prevent them from accessing registration and redirect home
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        from .forms import RegisterForm
        form = RegisterForm(request.POST) # Bind POST data to the registration form
        
        if form.is_valid():
            user = form.save() # Commit the new User to the database (password is already hashed)
            
            # Ensure a UserProfile is created for storing phone numbers and cities
            UserProfile.objects.get_or_create(user=user)
            
            # Authenticate and log the user into the current session
            login(request, user)
            
            # Dispatch a success alert toast to display on the home template
            messages.success(request, f"Welcome to Grodiur, {user.first_name}! 🎉")
            return redirect('home')
        else:
            # Dispatch an error message to let the customer review validation issues
            messages.error(request, "Please fix the errors below.")
    else:
        from .forms import RegisterForm
        form = RegisterForm() # Instantiate an empty registration form for GET requests
        
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    CUSTOMER LOGIN VIEW
    -------------------
    - GET request: Renders the standard login page.
    - POST request: Authenticates credentials using Django's AuthenticationForm.
      - On success: Logs in the user and redirects to the homepage or the previously requested URL.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        from .forms import LoginForm
        # Bind the incoming POST payload and session metadata to the form
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user() # Retrieve the authenticated User object
            login(request, user)   # Write the authenticated user ID to the session database
            messages.success(request, f"Welcome back, {user.first_name}! 🛒")
            
            # Redirect to the target URL if they were redirected to login, else default to 'home'
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, "Invalid username or password.")
    else:
        from .forms import LoginForm
        form = LoginForm()
        
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    LOGOUT CONTROLLER
    -----------------
    Flushes the current user's session data from the server, invalidating 
    their authenticated state, and redirects them to the login screen.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


def custom_login_required(view_func):
    """
    DECORATOR: SECURE REST API LOGIN GATE
    -------------------------------------
    This custom decorator intercepts requests to protected views.
    - If the user is authenticated, execution continues normally.
    - If not authenticated, instead of redirecting (which breaks AJAX/frontend calls),
      it returns a standardized 401 HTTP Unauthorized JSON response.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'login_required': True, 
                'message': 'Please login to continue.'
            }, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@custom_login_required
def profile_view(request):
    """
    USER DASHBOARD PROFILE VIEW
    ---------------------------
    Aggregates orders count metrics (total and completed) for the logged-in user 
    and passes them to the profile management template.
    """
    total_orders = request.user.orders.count()
    completed_orders = request.user.orders.filter(status='delivered').count()
    return render(request, 'accounts/profile.html', {
        'total_orders': total_orders,
        'completed_orders': completed_orders
    })


@custom_login_required
def saved_addresses(request):
    """
    DYNAMIC SHIPPING ADDRESS MANAGER
    --------------------------------
    Handles listing, adding, editing, and deleting customer delivery locations.
    It supports structured JSON request bodies for highly interactive single-page operation.
    """
    from .models import Address
    # Query database to retrieve only the addresses belonging to this specific user
    addresses = Address.objects.filter(user=request.user)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            # CASE A: Add a new address record
            if action == 'add':
                Address.objects.create(
                    user=request.user, 
                    **{k:v for k,v in data.items() if k not in ['action', 'id']}
                )
                return JsonResponse({'success': True})
                
            # CASE B: Update an existing address details
            elif action == 'edit':
                Address.objects.filter(
                    id=data.get('id'), 
                    user=request.user
                ).update(**{k:v for k,v in data.items() if k not in ['action', 'id']})
                return JsonResponse({'success': True})
                
            # CASE C: Delete an address record
            elif action == 'delete':
                Address.objects.filter(id=data.get('id'), user=request.user).delete()
                return JsonResponse({'success': True})
                
            # CASE D: Set an address as the default selection during checkout
            elif action == 'set_default':
                # First, strip 'default' status from all other addresses owned by this user
                Address.objects.filter(user=request.user).update(is_default=False)
                # Next, mark this specific address as default
                Address.objects.filter(id=data.get('id'), user=request.user).update(is_default=True)
                return JsonResponse({'success': True})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return render(request, 'accounts/saved_addresses.html', {'addresses': addresses})


@custom_login_required
def payment_methods(request):
    """
    SAVED PAYMENT METHODS CONTROLLER
    --------------------------------
    Renders the UI list of payment configurations (e.g. Razorpay payment profiles).
    """
    return render(request, 'accounts/payment_methods.html')


@custom_login_required
def wishlist(request):
    """
    WISHLIST DISPLAY CONTROLLER
    ---------------------------
    Retrieves and displays all product listings added to the user's wishlist.
    """
    from products.models import Wishlist
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'accounts/wishlist.html', {'items': items})


@custom_login_required
def add_to_wishlist(request, product_id):
    """
    ADD PRODUCT TO WISHLIST
    -----------------------
    Adds a select grocery item to the logged-in user's personalized bookmark wishlist.
    Safely prevents duplicate entries using ORM get_or_create.
    """
    from products.models import Product, Wishlist
    product = get_object_or_404(Product, id=product_id)
    # Check/Create the link; prevents multiple records of same product in wishlist
    _, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if created: 
        messages.success(request, f"Added {product.name} to wishlist.")
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))


@custom_login_required
def remove_from_wishlist(request, product_id):
    """
    REMOVE PRODUCT FROM WISHLIST
    ----------------------------
    Removes the specified product link from the customer's bookmark table.
    """
    from products.models import Wishlist
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    messages.success(request, "Removed from wishlist.")
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))


@custom_login_required
def settings_view(request):
    """
    ACCOUNT SECURITY SETTINGS
    -------------------------
    Renders UI panels allowing customers to update security configurations.
    """
    return render(request, 'accounts/settings.html')


@custom_login_required
def api_user_me(request):
    """
    JSON API: CURRENT USER STATE
    ----------------------------
    Endpoint returning vital user information for frontend templates or dashboard cards.
    """
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return JsonResponse({
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'phone': profile.phone or '',
    })


@custom_login_required
def api_user_update(request):
    """
    JSON API: UPDATE ACCOUNT INFO
    -----------------------------
    Endpoint receiving AJAX JSON payload containing first and last names.
    Validates, updates the authenticated User model, and returns the modified state.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        fname = data.get('firstName', '').strip()
        lname = data.get('lastName', '').strip()
        
        if not fname: 
            return JsonResponse({'success': False, 'error': 'First name is required'}, status=400)
            
        request.user.first_name = fname
        request.user.last_name = lname
        request.user.save() # Write modifications to the standard auth User table
        
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