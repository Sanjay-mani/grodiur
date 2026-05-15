from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.views import custom_login_required
from products.models import Product
from .models import Cart, CartItem
import json


@custom_login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@custom_login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if not product.is_available:
        if request.headers.get('Content-Type') == 'application/json' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'This product is currently unavailable.'})
        messages.error(request, "This product is currently unavailable.")
        return redirect(request.META.get('HTTP_REFERER', 'product_list'))

    quantity_to_add = 1
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if 'quantity' in data:
                quantity_to_add = int(data['quantity'])
        except Exception:
            quantity_to_add = int(request.POST.get('quantity', 1))

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, product=product
    )
    if not item_created:
        cart_item.quantity += quantity_to_add
    else:
        if quantity_to_add > 1:
            cart_item.quantity = quantity_to_add
        elif quantity_to_add <= 0:
            cart_item.delete()
            return redirect(request.META.get('HTTP_REFERER', 'product_list'))

    if cart_item.quantity <= 0:
        cart_item.delete()
    else:
        cart_item.save()
            
    messages.success(request, f"Added {product.name} to your cart.")
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))


@custom_login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart_detail')


@custom_login_required
def update_cart_ajax(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart = cart_item.cart
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            item_qty = cart_item.quantity
            item_subtotal = float(cart_item.get_subtotal())

            if action == 'increase':
                if not cart_item.product.is_available:
                    return JsonResponse({'success': False, 'error': 'This product is currently unavailable.'})
                cart_item.quantity += 1
                cart_item.save()
                item_qty = cart_item.quantity
                item_subtotal = float(cart_item.get_subtotal())
            elif action == 'decrease':
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                    item_qty = cart_item.quantity
                    item_subtotal = float(cart_item.get_subtotal())
                else:
                    cart_item.delete()
                    item_qty = 0
                    item_subtotal = 0
                    if not cart.items.exists():
                        cart.coupon = None
                        cart.save()
                    
            return JsonResponse({
                'success': True,
                'item_quantity': item_qty,
                'item_subtotal': item_subtotal,
                'total_items': cart.get_total_items(),
                'total_products': cart.get_total_products(),
                'mrp_total': float(cart.get_total_mrp()),
                'discount': float(cart.get_discount()),
                'coupon_discount': float(cart.get_coupon_discount()),
                'delivery_fee': float(cart.get_delivery_fee()),
                'total_savings': float(cart.get_total_savings()),
                'final_total': float(cart.get_final_total()),
                'free_delivery_threshold': 199,
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@custom_login_required
def apply_coupon(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '').strip()
            from .models import Coupon
            
            cart = get_object_or_404(Cart, user=request.user)
            
            try:
                from django.utils import timezone
                coupon = Coupon.objects.get(code__iexact=code, is_active=True)
                if coupon.expiry_date and coupon.expiry_date < timezone.now():
                    return JsonResponse({'success': False, 'message': 'Coupon has expired.'})
                
                if cart.get_item_total() >= coupon.min_order_value:
                    cart.coupon = coupon
                    cart.save()
                    return JsonResponse({
                        'success': True,
                        'message': f"Coupon '{code}' applied successfully!",
                        'total_items': cart.get_total_items(),
                        'total_products': cart.get_total_products(),
                        'mrp_total': float(cart.get_total_mrp()),
                        'discount': float(cart.get_discount()),
                        'coupon_discount': float(cart.get_coupon_discount()),
                        'delivery_fee': float(cart.get_delivery_fee()),
                        'total_savings': float(cart.get_total_savings()),
                        'final_total': float(cart.get_final_total()),
                        'free_delivery_threshold': 199,
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': f"Minimum order value for this coupon is ₹{coupon.min_order_value}"
                    })
            except Coupon.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Invalid or expired coupon.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@custom_login_required
def get_cart_count(request):
    try:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return JsonResponse({'success': True, 'total_items': cart.get_total_items()})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@custom_login_required
def remove_coupon(request):
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user)
        cart.coupon = None
        cart.save()
        return JsonResponse({
            'success': True,
            'message': 'Coupon removed.',
            'total_items': cart.get_total_items(),
            'total_products': cart.get_total_products(),
            'mrp_total': float(cart.get_total_mrp()),
            'discount': float(cart.get_discount()),
            'coupon_discount': 0,
            'delivery_fee': float(cart.get_delivery_fee()),
            'total_savings': float(cart.get_total_savings()),
            'final_total': float(cart.get_final_total()),
            'free_delivery_threshold': 199,
        })
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@custom_login_required
def api_cart_json(request):
    """GET /cart/api/json/ - Return full cart state for local synchronization."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = []
    for item in cart.items.all():
        items.append({
            'product_id': item.product.id,
            'product_name': item.product.name,
            'price': float(item.product.price),
            'image': item.product.image.url if item.product.image else None,
            'quantity': item.quantity,
            'subtotal': float(item.get_subtotal())
        })
    
    return JsonResponse({
        'total_items': cart.get_total_items(),
        'total_products': cart.get_total_products(),
        'mrp_total': float(cart.get_total_mrp()),
        'discount': float(cart.get_discount()),
        'coupon_discount': float(cart.get_coupon_discount()),
        'delivery_fee': float(cart.get_delivery_fee()),
        'final_total': float(cart.get_final_total()),
        'items': items
    })