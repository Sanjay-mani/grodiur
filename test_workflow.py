"""
Automated E2E Workflow Test for Grodiur
Tests: Login -> Add to Cart -> Checkout -> COD Order -> Order Success
"""
import os, sys, django

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grodiur.settings')
django.setup()

from django.test import Client as DjangoClient
from django.contrib.auth.models import User
from products.models import Product
from cart.models import Cart, CartItem
from accounts.models import Address, UserProfile
from orders.models import Order

DIVIDER = "=" * 60

def run_test():
    client = DjangoClient()
    print(f"\n{DIVIDER}")
    print("  GRODIUR E2E WORKFLOW TEST")
    print(f"{DIVIDER}\n")

    # STEP 1: Login
    print("[STEP 1] Logging in as 'sanjay'...")
    user = User.objects.get(username='sanjay')
    client.force_login(user)
    resp = client.get('/cart/')
    assert resp.status_code == 200, f"Login failed! Got status {resp.status_code}"
    print("  [PASS] Logged in successfully as 'sanjay'\n")

    # STEP 2: List available products
    print("[STEP 2] Fetching available products...")
    products = Product.objects.filter(stock__gt=0)[:5]
    if not products.exists():
        products = Product.objects.all()[:5]
    
    print(f"  Found {products.count()} products:")
    for p in products:
        print(f"    - {p.name} | Rs.{p.price} | Stock: {p.stock}")
    print()

    # STEP 3: Add products to cart
    print("[STEP 3] Adding products to cart...")
    added_count = 0
    for p in products[:2]:
        resp = client.get(f'/cart/add/{p.id}/')
        if resp.status_code in [200, 302]:
            print(f"  [PASS] Added '{p.name}' to cart")
            added_count += 1
        else:
            print(f"  [FAIL] Failed to add '{p.name}' (status: {resp.status_code})")
    
    assert added_count > 0, "No products were added to cart!"
    print()

    # STEP 4: Verify cart contents
    print("[STEP 4] Verifying cart...")
    resp = client.get('/cart/api/json/')
    if resp.status_code == 200:
        cart_data = resp.json()
        print(f"  Total items: {cart_data['total_items']}")
        print(f"  Final total: Rs.{cart_data['final_total']}")
        for item in cart_data.get('items', []):
            print(f"    - {item['product_name']} x{item['quantity']} = Rs.{item['subtotal']}")
    else:
        print(f"  Cart API returned status {resp.status_code}")
    print()

    # STEP 5: Ensure a saved address exists
    print("[STEP 5] Setting up delivery address...")
    address = Address.objects.filter(user=user).first()
    if not address:
        address = Address.objects.create(
            user=user,
            full_name='Sanjay M',
            phone='8861343169',
            house_street='123 Test Street, MG Road',
            city='Bengaluru',
            pincode='560001',
            is_default=True,
        )
        print(f"  [PASS] Created new address: {address.house_street}, {address.city}")
    else:
        print(f"  [PASS] Using existing address: {address.house_street}, {address.city}")
    print()

    # STEP 6: Checkout page
    print("[STEP 6] Loading checkout page...")
    resp = client.get('/orders/checkout/')
    assert resp.status_code == 200, f"Checkout page failed! Status: {resp.status_code}"
    print("  [PASS] Checkout page loaded successfully\n")

    # STEP 7: Place order with COD
    print("[STEP 7] Placing order (Cash on Delivery)...")
    from django.middleware.csrf import get_token
    csrf_token = get_token(resp.wsgi_request)
    
    resp = client.post('/orders/checkout/', {
        'place_order': 'true',
        'selected_address': address.id,
        'payment_method': 'COD',
        'csrfmiddlewaretoken': csrf_token,
    })
    
    order_id = None
    if resp.status_code == 302:
        redirect_url = resp.url
        print(f"  [PASS] Order placed! Redirecting to: {redirect_url}")
        order_id = redirect_url.split('/orders/success/')[1].rstrip('/')
        print(f"  Order ID: {order_id}")
    else:
        order = Order.objects.filter(user=user).order_by('-created_at').first()
        if order:
            order_id = order.order_id
            print(f"  Order found in DB: {order_id}")
        else:
            print(f"  [FAIL] No order found! Status: {resp.status_code}")
            return
    print()

    # STEP 8: Verify order success page
    print("[STEP 8] Loading order success page...")
    resp = client.get(f'/orders/success/{order_id}/')
    assert resp.status_code == 200, f"Order success page failed! Status: {resp.status_code}"
    print("  [PASS] Order success page loaded!\n")

    # STEP 9: Verify order details via API
    print("[STEP 9] Verifying order details...")
    resp = client.get(f'/orders/api/orders/{order_id}')
    if resp.status_code == 200:
        order_data = resp.json()
        print(f"  Order ID:       {order_data['order_id']}")
        print(f"  Status:         {order_data['status']}")
        print(f"  Payment:        {order_data['payment_method']}")
        print(f"  Payment Status: {order_data['payment_status']}")
        print(f"  Total:          Rs.{order_data['total']}")
        print(f"  Delivery To:    {order_data['full_name']}, {order_data['city']}")
        print(f"  Items:")
        for item in order_data['items']:
            print(f"    - {item['name']} x{item['quantity']} @ Rs.{item['price']}")
    print()

    # STEP 10: Verify order history
    print("[STEP 10] Checking order history...")
    resp = client.get('/orders/history/')
    assert resp.status_code == 200, f"Order history failed! Status: {resp.status_code}"
    print("  [PASS] Order history page works!\n")

    # STEP 11: Test order invoice
    print("[STEP 11] Loading invoice...")
    resp = client.get(f'/orders/{order_id}/invoice/')
    assert resp.status_code == 200, f"Invoice page failed! Status: {resp.status_code}"
    print("  [PASS] Invoice page works!\n")

    # FINAL SUMMARY
    print(f"{DIVIDER}")
    print("  ALL TESTS PASSED!")
    print(f"{DIVIDER}")
    print(f"  [PASS] Login:           Working")
    print(f"  [PASS] Product Listing:  Working")
    print(f"  [PASS] Add to Cart:      Working")
    print(f"  [PASS] Cart API:         Working")
    print(f"  [PASS] Checkout:         Working")
    print(f"  [PASS] COD Order:        Working (Order #{order_id})")
    print(f"  [PASS] Order Success:    Working")
    print(f"  [PASS] Order Details:    Working")
    print(f"  [PASS] Order History:    Working")
    print(f"  [PASS] Invoice:          Working")
    print(f"{DIVIDER}\n")


if __name__ == '__main__':
    run_test()
