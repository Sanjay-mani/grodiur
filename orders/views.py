from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from accounts.views import custom_login_required
from django.contrib import messages
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem, SupportTicket
import razorpay
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

def get_razorpay_client():
    from dotenv import load_dotenv
    import os
    from django.conf import settings
    # Force reload of .env to ensure new keys are used even without server restart
    env_path = settings.BASE_DIR / '.env'
    load_dotenv(env_path, override=True)
    key_id = os.environ.get('RAZORPAY_KEY_ID', settings.RAZORPAY_KEY_ID)
    key_secret = os.environ.get('RAZORPAY_KEY_SECRET', settings.RAZORPAY_KEY_SECRET)
    return razorpay.Client(auth=(key_id, key_secret))


@custom_login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect('product_list')

    from accounts.models import Address
    saved_addresses = Address.objects.filter(user=request.user)

    if request.method == 'POST':
        # Check if adding a new address
        if 'add_address' in request.POST:
            full_name = request.POST.get('full_name')
            phone = request.POST.get('phone')
            house_street = request.POST.get('house_street')
            city = request.POST.get('city')
            pincode = request.POST.get('pincode')
            is_default = request.POST.get('is_default') == 'on'

            Address.objects.create(
                user=request.user,
                full_name=full_name,
                phone=phone,
                house_street=house_street,
                city=city,
                pincode=pincode,
                is_default=is_default or not saved_addresses.exists()
            )
            messages.success(request, "Address saved successfully.")
            return redirect('checkout')

        # Or Placing Order
        elif 'place_order' in request.POST:
            # Check for unavailable products
            unavailable_items = [item for item in cart.items.all() if not item.product.is_available]
            if unavailable_items:
                messages.error(request, "Some items in your cart are currently unavailable. Please remove them before checking out.")
                return redirect('cart_detail')

            address_id = request.POST.get('selected_address')
            payment_method = request.POST.get('payment_method', 'COD')

            if not address_id:
                messages.error(request, "Please select a delivery address.")
                return redirect('checkout')

            selected_address = get_object_or_404(Address, id=address_id, user=request.user)

            # Create the order
            order = Order.objects.create(
                user=request.user,
                full_name=selected_address.full_name,
                phone=selected_address.phone,
                address=selected_address.house_street,
                city=selected_address.city,
                pincode=selected_address.pincode,
                payment_method=payment_method,
                payment_status='pending' if payment_method == 'COD' else 'paid',
                subtotal=cart.get_item_total(),
                mrp_total=cart.get_total_mrp(),
                coupon=cart.coupon,
                coupon_discount=cart.get_coupon_discount(),
                delivery_fee=cart.get_delivery_fee(),
                total_price=cart.get_final_total()
            )

            # Copy cart items to order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            # Clear the cart
            cart.items.all().delete()
            if cart.coupon:
                cart.coupon = None
                cart.save()

            return redirect('order_success', order_id=order.order_id)

    context = {
        'cart': cart,
        'saved_addresses': saved_addresses,
    }
    return render(request, 'orders/checkout.html', context)


@custom_login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@custom_login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related('items__product'),
        order_id=order_id,
        user=request.user
    )

    # Use stored totals (Single Source of Truth)
    item_total = order.subtotal
    discount = order.coupon_discount
    delivery_fee = order.delivery_fee
    grand_total = order.total_price
    tracking_step = order.get_tracking_step()

    context = {
        'order': order,
        'item_total': item_total,
        'discount': discount,
        'delivery_fee': delivery_fee,
        'grand_total': grand_total,
        'tracking_step': tracking_step,
    }
    return render(request, 'orders/order_detail.html', context)


@custom_login_required
def order_history(request):
    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related('items__product').order_by('-created_at')

    # Annotate each order with tracking step for the template
    for order in orders:
        order.tracking_step = order.get_tracking_step()

    return render(request, 'orders/order_history.html', {'orders': orders})


@custom_login_required
def order_invoice(request, order_id):
    """Render a clean, printable HTML invoice for the given order."""
    order = get_object_or_404(
        Order.objects.prefetch_related('items__product'),
        order_id=order_id,
        user=request.user
    )
    context = {
        'order': order,
        'item_total': order.subtotal,
    }
    return render(request, 'orders/invoice.html', context)


@custom_login_required
def order_again(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    for item in order.items.all():
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=item.product
        )
        if not created:
            cart_item.quantity += item.quantity
        else:
            cart_item.quantity = item.quantity
        cart_item.save()

    messages.success(request, f"Items from Order #{order.order_id} have been added to your cart.")
    return redirect('cart_detail')


@custom_login_required
def submit_support_ticket(request, order_id):
    """AJAX POST — create a SupportTicket for the given order."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    issue_type = request.POST.get('issue_type', 'other')
    message = request.POST.get('message', '').strip()

    if not message:
        return JsonResponse({'success': False, 'error': 'Message cannot be empty.'})

    SupportTicket.objects.create(
        user=request.user,
        order=order,
        issue_type=issue_type,
        message=message,
    )
    return JsonResponse({'success': True, 'message': 'Your support ticket has been submitted. We will get back to you shortly.'})


# --- API ENDPOINTS ---

@custom_login_required
def api_recent_orders(request):
    """GET /api/recent-orders/"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    data = []
    for o in orders:
        data.append({
            'order_id': o.order_id,
            'total_price': float(o.total_price),
            'status': o.get_status_display(),
            'created_at': o.created_at.isoformat(),
        })
    return JsonResponse(data, safe=False)


@custom_login_required
def api_orders(request):
    """GET /api/orders"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    data = []
    for o in orders:
        data.append({
            'order_id': o.order_id,
            'total': float(o.total_price),
            'status': o.status,
            'created_at': o.created_at.isoformat(),
            'items_count': o.items.count()
        })
    return JsonResponse(data, safe=False)

@custom_login_required
def api_order_detail_json(request, order_id):
    """GET /api/orders/:id - Supports both numeric ID and string order_id"""
    if order_id.isdigit():
        order = get_object_or_404(Order, id=int(order_id), user=request.user)
    else:
        order = get_object_or_404(Order, order_id=order_id, user=request.user)
        
    items = []
    for item in order.items.all():
        items.append({
            'name': item.product.name,
            'quantity': item.quantity,
            'price': float(item.price),
            'image': item.product.image.url if item.product.image else None,
            'unit': item.product.unit,
            'subtotal': float(item.get_subtotal())
        })
    
    # Single Source of Truth for COD payment logic
    payment_status = order.payment_status
    if order.payment_method == 'COD':
        payment_status = 'paid' if order.status == 'delivered' else 'pending'

    return JsonResponse({
        '_id': order.id,
        'order_id': order.order_id,
        'status': order.status,
        'tracking_step': order.get_tracking_step(),
        'full_name': order.full_name,
        'phone': order.phone,
        'address_line': order.address,
        'city': order.city,
        'pincode': order.pincode,
        'item_total': float(order.subtotal),
        'discount': float(order.coupon_discount or 0),
        'delivery_fee': float(order.delivery_fee),
        'total': float(order.total_price),
        'payment_method': order.payment_method,
        'payment_status': payment_status,
        'created_at': order.created_at.isoformat(),
        'items': items
    })

@csrf_exempt
@custom_login_required
def create_razorpay_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            address_id = data.get("address_id")
            
            if not address_id:
                return JsonResponse({"success": False, "error": "Delivery address not selected"})
                
            from accounts.models import Address
            selected_address = get_object_or_404(Address, id=address_id, user=request.user)
            cart = get_object_or_404(Cart, user=request.user)
            
            if not cart.items.exists():
                return JsonResponse({"success": False, "error": "Your cart is empty!"})
                
            # Check for unavailable products
            unavailable_items = [item for item in cart.items.all() if not item.product.is_available]
            if unavailable_items:
                return JsonResponse({"success": False, "error": "Some items in your cart are currently unavailable."})
                
            # Pre-create the Django order to guarantee record conservation
            order = Order.objects.create(
                user=request.user,
                full_name=selected_address.full_name,
                phone=selected_address.phone,
                address=selected_address.house_street,
                city=selected_address.city,
                pincode=selected_address.pincode,
                payment_method='ONLINE',
                payment_status='pending',
                subtotal=cart.get_item_total(),
                mrp_total=cart.get_total_mrp(),
                coupon=cart.coupon,
                coupon_discount=cart.get_coupon_discount(),
                delivery_fee=cart.get_delivery_fee(),
                total_price=cart.get_final_total()
            )
            
            # Copy cart items to order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                
            # Initialize Razorpay live order
            amount = int(float(cart.get_final_total()) * 100)
            
            if amount < 100:
                return JsonResponse({"success": False, "error": "Amount must be at least 1 INR (100 paise)"}, status=400)
                
            try:
                client = get_razorpay_client()
                razorpay_order = client.order.create({
                    "amount": amount,
                    "currency": "INR",
                    "receipt": str(order.order_id),
                    "payment_capture": 1
                })
            except razorpay.errors.BadRequestError as e:
                print(f"Razorpay BadRequestError: {e}")
                return JsonResponse({"success": False, "error": f"Razorpay API error: {str(e)}"}, status=500)
            except Exception as e:
                print(f"Razorpay Error: {e}")
                if 'unauthorized' in str(e).lower() or 'auth' in str(e).lower():
                    return JsonResponse({"success": False, "error": "Invalid Razorpay Keys. Please use valid LIVE keys."}, status=401)
                return JsonResponse({"success": False, "error": str(e)}, status=500)
            
            # Save the Razorpay Order ID on the pre-created Django order
            order.razorpay_order_id = razorpay_order["id"]
            order.save()
            
            return JsonResponse({
                "success": True,
                "key": settings.RAZORPAY_KEY_ID,
                "amount": razorpay_order["amount"],
                "order_id": razorpay_order["id"]
            })
        except Exception as e:
            print(f"Checkout Backend Error: {e}")
            if 'unauthorized' in str(e).lower() or 'auth' in str(e).lower():
                return JsonResponse({"success": False, "error": "Invalid Razorpay Keys. Please use valid LIVE keys."}, status=401)
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

@csrf_exempt
@custom_login_required
def payment_success(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Verify Razorpay Signature
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_signature = data.get('razorpay_signature')
            
            if not razorpay_order_id or not razorpay_payment_id or not razorpay_signature:
                return JsonResponse({"success": False, "error": "Missing signature fields"}, status=400)

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            
            try:
                client = get_razorpay_client()
                client.utility.verify_payment_signature(params_dict)
            except Exception:
                return JsonResponse({"success": False, "error": "Invalid payment signature"}, status=400)
            
            # Find the pre-created Django order
            order = get_object_or_404(Order, razorpay_order_id=razorpay_order_id, user=request.user)
            
            if order.payment_status != 'paid':
                order.payment_status = 'paid'
                order.razorpay_payment_id = razorpay_payment_id
                order.razorpay_signature = razorpay_signature
                order.paid_at = timezone.now()
                order.save()
                
                # Clear the cart
                cart = get_object_or_404(Cart, user=request.user)
                cart.items.all().delete()
                if cart.coupon:
                    cart.coupon = None
                    cart.save()
                
            return JsonResponse({"success": True, "order_id": order.order_id})
            
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

@csrf_exempt
def razorpay_webhook(request):
    """Secure Razorpay webhook endpoint verifying hmac signatures for absolute data integrity."""
    if request.method == "POST":
        webhook_signature = request.headers.get("X-Razorpay-Signature")
        webhook_secret = getattr(settings, 'RAZORPAY_WEBHOOK_SECRET', None)
        
        # Verify webhook signature using the SDK if configured in .env
        if webhook_secret and webhook_signature:
            try:
                client = get_razorpay_client()
                client.utility.verify_webhook_signature(
                    request.body.decode('utf-8'),
                    webhook_signature,
                    webhook_secret
                )
            except Exception:
                return HttpResponse("Invalid Webhook Signature", status=400)
        
        try:
            payload = json.loads(request.body)
            event = payload.get("event")
            
            if event == "payment.captured":
                payment_entity = payload["payload"]["payment"]["entity"]
                razorpay_order_id = payment_entity.get("order_id")
                razorpay_payment_id = payment_entity.get("id")
                razorpay_signature = webhook_signature or ""
                
                try:
                    order = Order.objects.get(razorpay_order_id=razorpay_order_id)
                    if order.payment_status != 'paid':
                        order.payment_status = 'paid'
                        order.razorpay_payment_id = razorpay_payment_id
                        order.razorpay_signature = razorpay_signature
                        order.paid_at = timezone.now()
                        order.save()
                        
                        # Clear user's cart securely
                        try:
                            cart = Cart.objects.get(user=order.user)
                            cart.items.all().delete()
                            if cart.coupon:
                                cart.coupon = None
                                cart.save()
                        except Cart.DoesNotExist:
                            pass
                except Order.DoesNotExist:
                    pass
                    
            elif event == "payment.failed":
                payment_entity = payload["payload"]["payment"]["entity"]
                razorpay_order_id = payment_entity.get("order_id")
                try:
                    order = Order.objects.get(razorpay_order_id=razorpay_order_id)
                    if order.payment_status != 'paid':
                        order.payment_status = 'failed'
                        order.save()
                except Order.DoesNotExist:
                    pass
                    
        except Exception as e:
            return HttpResponse(str(e), status=500)
            
        return HttpResponse("OK", status=200)
    return HttpResponse("Invalid Method", status=400)

@custom_login_required
def latest_order_success(request):
    """Render success page for the latest order (handles redirects from Razorpay popup)."""
    order = Order.objects.filter(user=request.user).order_by('-created_at').first()
    if not order:
        return redirect('home')
    return render(request, 'orders/order_success.html', {'order': order})