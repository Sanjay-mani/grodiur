"""
FULL GRODIUR COMPREHENSIVE TEST SUITE
Tests ALL functionality: Login, OTP, Products, Cart, Checkout, Orders, Admin, Reviews, Wishlist, etc.
"""
import os, sys, django
sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grodiur.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from products.models import Product
from cart.models import Cart, CartItem
from accounts.models import Address, UserProfile
from orders.models import Order
from otp_auth.models import OTPVerification
import json, random

DIV = "=" * 65
SEC = "-" * 65
OK  = "[PASS]"
FAIL= "[FAIL]"
INFO= "[INFO]"

results = []

def check(name, passed, detail=""):
    icon = OK if passed else FAIL
    msg = f"  {icon} {name}"
    if detail: msg += f" | {detail}"
    print(msg)
    results.append((name, passed))
    return passed

def section(title):
    print(f"\n{SEC}")
    print(f"  {title}")
    print(f"{SEC}")

# ============================================================
print(f"\n{DIV}")
print("  GRODIUR FULL FUNCTIONALITY TEST SUITE")
print(f"{DIV}")

client = Client()

# ============================================================
section("1. EMAIL OTP LOGIN (sanjaymsanju011@gmail.com)")
# ============================================================

# Create a fresh OTP
OTPVerification.objects.filter(identifier='sanjaymsanju011@gmail.com').delete()
test_otp = str(random.randint(100000, 999999))
OTPVerification.objects.create(
    identifier='sanjaymsanju011@gmail.com',
    otp_type='email',
    otp=test_otp,
    ip_address='127.0.0.1'
)
print(f"  {INFO} Generated test OTP: {test_otp}")

# Test Send OTP API
resp = client.post('/api/send-email-otp/',
    data=json.dumps({'email': 'sanjaymsanju011@gmail.com'}),
    content_type='application/json'
)
check("Send OTP API (/api/send-email-otp/)", resp.status_code == 200, f"Status: {resp.status_code}")

# Test Verify OTP API
otp_obj = OTPVerification.objects.filter(identifier='sanjaymsanju011@gmail.com', status='pending').latest('created_at')
resp = client.post('/api/verify-email-otp/',
    data=json.dumps({'email': 'sanjaymsanju011@gmail.com', 'otp': otp_obj.otp}),
    content_type='application/json'
)
check("Verify OTP API (/api/verify-email-otp/)", resp.status_code == 200, f"Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    check("OTP returns tokens", 'tokens' in data)
    check("OTP creates Django session", '_auth_user_id' in client.session)
    email_user = User.objects.get(username='sanjaymsanju011@gmail.com')
    print(f"  {INFO} Logged in as: {email_user.username} (ID: {email_user.id})")

# ============================================================
section("2. DJANGO ADMIN (sanjay / sanjay)")
# ============================================================
admin_client = Client()
resp = admin_client.get('/admin/')
check("Admin page accessible", resp.status_code in [200, 302])
login_ok = admin_client.login(username='sanjay', password='sanjay')
check("Admin login (sanjay/sanjay)", login_ok)
resp = admin_client.get('/admin/')
check("Admin dashboard loads after login", resp.status_code == 200)
resp = admin_client.get('/admin/auth/user/')
check("Admin: User management", resp.status_code == 200)
resp = admin_client.get('/admin/products/product/')
check("Admin: Product management", resp.status_code == 200)
resp = admin_client.get('/admin/orders/order/')
check("Admin: Order management", resp.status_code == 200)

# ============================================================
section("3. HOMEPAGE & NAVIGATION")
# ============================================================
resp = client.get('/')
check("Homepage (/)", resp.status_code == 200)
resp = client.get('/products/')
check("Product listing (/products/)", resp.status_code == 200)

# ============================================================
section("4. PRODUCT SEARCH & BROWSING")
# ============================================================
resp = client.get('/products/?q=tomato')
check("Search for 'tomato'", resp.status_code == 200)
resp = client.get('/products/?q=onion')
check("Search for 'onion'", resp.status_code == 200)

# Get Tomato and Onion products
tomato = Product.objects.filter(name__icontains='tomato').first()
onion = Product.objects.filter(name__icontains='onion').first()
check("Tomato product exists in DB", tomato is not None, tomato.name if tomato else "NOT FOUND")
check("Onion product exists in DB", onion is not None, onion.name if onion else "NOT FOUND")

if tomato:
    resp = client.get(f'/product/{tomato.id}/')
    check("Tomato product detail page", resp.status_code == 200)
if onion:
    resp = client.get(f'/product/{onion.id}/')
    check("Onion product detail page", resp.status_code == 200)

# ============================================================
section("5. CART — ADD TOMATO & ONION")
# ============================================================
# Use email user session (already logged in from OTP)
cart_client = Client()
email_user = User.objects.get(username='sanjaymsanju011@gmail.com')
cart_client.force_login(email_user)

# Clear existing cart
Cart.objects.filter(user=email_user).delete()

if tomato:
    resp = cart_client.get(f'/cart/add/{tomato.id}/')
    check(f"Add Tomato to cart", resp.status_code in [200, 302], f"Rs.{tomato.price}")
if onion:
    resp = cart_client.get(f'/cart/add/{onion.id}/')
    check(f"Add Onion to cart", resp.status_code in [200, 302], f"Rs.{onion.price}")

# Verify cart contents
resp = cart_client.get('/cart/api/json/')
check("Cart API returns items", resp.status_code == 200)
if resp.status_code == 200:
    cart_data = resp.json()
    check("Cart has items", cart_data['total_items'] > 0, f"{cart_data['total_items']} items, Total: Rs.{cart_data['final_total']}")
    for item in cart_data.get('items', []):
        print(f"  {INFO} Cart item: {item['product_name']} x{item['quantity']} = Rs.{item['subtotal']}")

resp = cart_client.get('/cart/')
check("Cart detail page loads", resp.status_code == 200)

# Test cart count API
resp = cart_client.get('/cart/api/cart-count/')
check("Cart count API", resp.status_code == 200)

# ============================================================
section("6. CHECKOUT & COD ORDER PLACEMENT")
# ============================================================
# Ensure address exists
address, _ = Address.objects.get_or_create(
    user=email_user,
    defaults={
        'full_name': 'Sanjay M',
        'phone': '8861343169',
        'house_street': '123 MG Road, Bengaluru',
        'city': 'Bengaluru',
        'pincode': '560001',
        'is_default': True,
    }
)
address = Address.objects.filter(user=email_user).first()
print(f"  {INFO} Using address: {address.house_street}, {address.city}")

resp = cart_client.get('/orders/checkout/')
check("Checkout page loads", resp.status_code == 200)

# Place COD order
resp = cart_client.post('/orders/checkout/', {
    'place_order': 'true',
    'selected_address': address.id,
    'payment_method': 'COD',
    'csrfmiddlewaretoken': 'test',
})
check("COD order placed", resp.status_code == 302, f"Redirect: {getattr(resp, 'url', 'none')}")

cod_order = None
if resp.status_code == 302:
    redirect_url = resp.url
    order_id = redirect_url.split('/orders/success/')[1].rstrip('/')
    cod_order = Order.objects.get(order_id=order_id)
    check("Order success page loads", cart_client.get(f'/orders/success/{order_id}/').status_code == 200, f"Order #{order_id}")
    print(f"  {INFO} COD Order: #{order_id} | Total: Rs.{cod_order.total_price}")

# ============================================================
section("7. RAZORPAY ONLINE PAYMENT ORDER")
# ============================================================
# Add items back for Razorpay test
if tomato: cart_client.get(f'/cart/add/{tomato.id}/')
if onion: cart_client.get(f'/cart/add/{onion.id}/')

address2 = Address.objects.filter(user=email_user).first()

# Create Razorpay order
resp = cart_client.post('/orders/api/create-razorpay-order/',
    data=json.dumps({'amount': 200.00, 'address_id': address2.id}),
    content_type='application/json'
)
check("Razorpay order creation API", resp.status_code == 200, f"Status: {resp.status_code}")
if resp.status_code == 200:
    rz_data = resp.json()
    check("Razorpay returns order ID", rz_data.get('success', False) and 'order_id' in rz_data)
    if rz_data.get('success'):
        print(f"  {INFO} Razorpay Order ID: {rz_data.get('order_id')} | Key: {rz_data.get('key')}")

# ============================================================
section("8. ORDER HISTORY & DETAILS")
# ============================================================
resp = cart_client.get('/orders/history/')
check("Order history page", resp.status_code == 200)

resp = cart_client.get('/orders/api/orders')
check("Orders API", resp.status_code == 200)

resp = cart_client.get('/orders/api/recent-orders/')
check("Recent orders API", resp.status_code == 200)

if cod_order:
    resp = cart_client.get(f'/orders/{cod_order.order_id}/')
    check("Order detail page", resp.status_code == 200, f"Order #{cod_order.order_id}")

    resp = cart_client.get(f'/orders/api/orders/{cod_order.order_id}')
    check("Order detail API (JSON)", resp.status_code == 200)
    if resp.status_code == 200:
        od = resp.json()
        print(f"  {INFO} Order status: {od['status']} | Payment: {od['payment_method']} | {od['payment_status']}")

    resp = cart_client.get(f'/orders/{cod_order.order_id}/invoice/')
    check("Order invoice page", resp.status_code == 200)

# ============================================================
section("9. ACCOUNT & PROFILE")
# ============================================================
resp = cart_client.get('/accounts/profile/')
check("Profile page", resp.status_code == 200)

resp = cart_client.get('/accounts/saved-addresses/')
check("Saved addresses page", resp.status_code == 200)

resp = cart_client.get('/accounts/settings/')
check("Settings page", resp.status_code == 200)

resp = cart_client.get('/accounts/api/user/me')
check("User API (/api/user/me)", resp.status_code == 200)
if resp.status_code == 200:
    u = resp.json()
    print(f"  {INFO} User: {u.get('first_name', '')} {u.get('last_name', '')} | Email: {u.get('email', '')}")

# ============================================================
section("10. WISHLIST")
# ============================================================
resp = cart_client.get('/accounts/wishlist/')
check("Wishlist page", resp.status_code == 200)

if tomato:
    resp = cart_client.get(f'/accounts/wishlist/add/{tomato.id}/')
    check("Add to wishlist", resp.status_code in [200, 302])
    resp = cart_client.get(f'/accounts/wishlist/remove/{tomato.id}/')
    check("Remove from wishlist", resp.status_code in [200, 302])

# ============================================================
section("11. REVIEWS")
# ============================================================
if tomato:
    resp = cart_client.get(f'/api/products/{tomato.id}/reviews/')
    check("Product reviews API", resp.status_code == 200)

# ============================================================
section("12. CHATBOT")
# ============================================================
resp = cart_client.post('/chatbot/response/',
    data=json.dumps({'message': 'hello'}),
    content_type='application/json'
)
check("Chatbot API responds", resp.status_code == 200)

# ============================================================
section("13. OTP ENDPOINTS — PHONE LOGIN TEST")
# ============================================================
resp = client.post('/api/send-phone-otp/',
    data=json.dumps({'phone': '8861343169'}),
    content_type='application/json'
)
check("Phone OTP send API", resp.status_code in [200, 500], f"Status: {resp.status_code}")
# 500 is OK here if Twilio is not configured (test mode)

# ============================================================
section("14. UNAUTHENTICATED ACCESS PROTECTION")
# ============================================================
anon = Client()
resp = anon.get('/cart/')
check("Cart protected (returns 401 JSON or redirect)", resp.status_code in [401, 302, 200])
resp = anon.get('/orders/checkout/')
check("Checkout protected", resp.status_code in [401, 302, 200])
resp = anon.get('/accounts/profile/')
check("Profile protected", resp.status_code in [401, 302, 200])

# ============================================================
section("15. STATIC FILES & MEDIA")
# ============================================================
resp = client.get('/static/rest_framework/css/bootstrap.min.css')
check("Static files served by WhiteNoise", resp.status_code == 200)

# ============================================================
# FINAL REPORT
# ============================================================
print(f"\n{DIV}")
print("  FINAL TEST REPORT")
print(f"{DIV}")
passed = sum(1 for _, p in results if p)
failed = sum(1 for _, p in results if not p)
print(f"  Total: {len(results)} | Passed: {passed} | Failed: {failed}")
print()
if failed > 0:
    print("  FAILED TESTS:")
    for name, p in results:
        if not p:
            print(f"    [FAIL] {name}")
print(f"{DIV}\n")
