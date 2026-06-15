# reviews/views.py
"""
GRODIUR - REVIEWS AND RATINGS MODULE
===================================
This module provides views for customers to submit product reviews and ratings.
It supports both traditional POST form submissions and modern asynchronous AJAX API requests.
All endpoints are secured to ensure only logged-in, authenticated shoppers can write or delete reviews.
"""

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
    """
    ADD PRODUCT REVIEW (Traditional Form Submission)
    ------------------------------------------------
    Triggered when a logged-in user submits a standard HTML form to rate a product.
    Uses 'update_or_create' so if the user has already rated this product, 
    it simply updates their existing rating and comments instead of duplicating records.
    """
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        # Save or update user review in the SQLite database
        Review.objects.update_or_create(
            user=request.user, 
            product=product,
            defaults={'rating': rating, 'comment': comment}
        )
        messages.success(request, 'Review added successfully!')
        
    return redirect('product_detail', product_id=product_id)


@login_required
def delete_review(request, review_id):
    """
    DELETE PRODUCT REVIEW
    ---------------------
    Deletes a review record. Restricts action to ensure a customer can only delete
    their own reviews (enforced by adding `user=request.user` to the DB query).
    """
    # Fetch the review ensuring it belongs strictly to the currently logged-in user
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_id = review.product.id
    review.delete() # Execute deletion command in SQLite
    
    messages.success(request, 'Review deleted.')
    return redirect('product_detail', product_id=product_id)


@login_required
def api_create_review(request):
    """
    JSON API: SUBMIT/UPDATE REVIEW (AJAX Gateway)
    ---------------------------------------------
    Receives JSON POST inputs containing rating, comments, product_id, and order_id.
    This enables highly interactive single-page reviews within the order history screens.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    try:
        product_id = request.POST.get('product_id')
        order_id = request.POST.get('order_id')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()
        
        # Validate that all required inputs are present
        if not all([product_id, rating, comment]):
            return JsonResponse({'success': False, 'error': 'Missing required fields'})
            
        product = get_object_or_404(Product, id=product_id)
        
        # Safely link the review to the corresponding order if one is provided
        order = get_object_or_404(Order, id=order_id, user=request.user) if (order_id and order_id != 'None') else None
        
        # Create or update the review record
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