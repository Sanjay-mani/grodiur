from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.http import JsonResponse
from reviews.models import Review
import json

def get_categories(request):
    categories = Category.objects.all().values('id', 'name', 'slug')
    return JsonResponse(list(categories), safe=False)


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Search
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    # Filter by category
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = Category.objects.filter(slug__iexact=category_slug).first()
        if selected_category:
            products = products.filter(category=selected_category)

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'query': query,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)


def product_detail_by_id(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)


def product_reviews_api(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'GET':
        reviews = Review.objects.filter(product=product).order_by('-created_at')
        reviews_data = [{
            'userName': review.user.get_full_name() or review.user.username,
            'rating': review.rating,
            'comment': review.comment,
            'createdAt': review.created_at.strftime("%b %d, %Y")
        } for review in reviews]
        return JsonResponse(reviews_data, safe=False)
    
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Login required'}, status=401)
        
        try:
            data = json.loads(request.body)
            rating = int(data.get('rating'))
            comment = data.get('comment', '').strip()
            
            if not rating or len(comment) < 5:
                return JsonResponse({'success': False, 'error': 'Invalid rating or comment (min 5 chars)'})
            
            review, created = Review.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={'rating': rating, 'comment': comment}
            )
            
            return JsonResponse({
                'success': True, 
                'review': {
                    'userName': request.user.get_full_name() or request.user.username,
                    'rating': review.rating,
                    'comment': review.comment,
                    'createdAt': review.created_at.strftime("%b %d, %Y")
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


def api_product_search(request):
    """Chatbot product search API with fuzzy matching."""
    query = request.GET.get('q', '').strip().lower()
    if not query or len(query) < 2:
        return JsonResponse([], safe=False)

    # Strip common plural suffixes for better matching
    search_terms = [query]
    if query.endswith('es'):
        search_terms.append(query[:-2])
    elif query.endswith('s'):
        search_terms.append(query[:-1])

    # Strip common prefixes like "show", "find", "need", "get", "buy"
    for prefix in ['show ', 'find ', 'need ', 'get ', 'buy ', 'i want ', 'search ']:
        if query.startswith(prefix):
            cleaned = query[len(prefix):].strip()
            if cleaned:
                search_terms.append(cleaned)
                if cleaned.endswith('es'):
                    search_terms.append(cleaned[:-2])
                elif cleaned.endswith('s'):
                    search_terms.append(cleaned[:-1])

    # Search with all terms using icontains
    from django.db.models import Q
    q_filter = Q()
    for term in search_terms:
        q_filter |= Q(name__icontains=term)
        q_filter |= Q(description__icontains=term)
        q_filter |= Q(category__name__icontains=term)

    products = Product.objects.filter(q_filter).distinct()[:8]

    results = []
    for p in products:
        results.append({
            'id': p.id,
            'name': p.name,
            'slug': p.slug,
            'price': str(p.price),
            'mrp_price': str(p.mrp_price) if p.mrp_price else None,
            'unit': p.unit,
            'stock': p.stock,
            'image': p.image.url if p.image else None,
            'category': p.category.name if p.category else '',
        })

    return JsonResponse(results, safe=False)