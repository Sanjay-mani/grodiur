# reviews/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Review
from products.models import Product
from orders.models import Order
from django.contrib import messages
import json

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.update_or_create(
            user=request.user, 
            product=product,
            defaults={'rating': rating, 'comment': comment}
        )
        messages.success(request, 'Review added successfully!')
    return redirect('product_detail', product_id=product_id)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_id = review.product.id
    review.delete()
    messages.success(request, 'Review deleted.')
    return redirect('product_detail', product_id=product_id)

@login_required
def api_create_review(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    try:
        product_id = request.POST.get('product_id')
        order_id = request.POST.get('order_id')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()
        
        if not all([product_id, rating, comment]):
            return JsonResponse({'success': False, 'error': 'Missing required fields'})
            
        product = get_object_or_404(Product, id=product_id)
        order = get_object_or_404(Order, id=order_id, user=request.user) if (order_id and order_id != 'None') else None
        
        # Check if user already reviewed this product for this order (or overall if unique_together is set)
        review, created = Review.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={
                'order': order,
                'rating': int(rating),
                'comment': comment
            }
        )
        
        return JsonResponse({'success': True, 'message': 'Review submitted successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})