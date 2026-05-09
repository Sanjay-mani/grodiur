from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from products.models import Product, Category
from orders.models import Order
import json
import re


def get_bot_response(message, user):
    message_lower = message.lower().strip()
    
    # 1. Order ID Detection (The most specific intent)
    order_id_pattern = r'GRO-\d{4}-\d+'
    order_match = re.search(order_id_pattern, message_lower, re.IGNORECASE)
    
    if order_match:
        order_id = order_match.group().upper()
        try:
            order = Order.objects.get(order_id=order_id)
            if order.user != user:
                return f"❌ Order **{order_id}** does not belong to this account."
            
            # We return a special prefix so the frontend knows to render a rich tracker
            return f"INTENT_TRACK_ORDER|{order.order_id}"
        except Order.DoesNotExist:
            return f"❌ Order **{order_id}** not found.\nPlease double-check the Order ID and try again."

    # 2. Greetings
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'namaste']):
        return f"👋 Hello {user.first_name}!\n\nI'm your Grodiur Assistant. I can help you track orders, search products, or assist with delivery and refunds.\n\nWhat can I do for you today?"

    # 3. Track Order Intent (When no ID is provided)
    if any(word in message_lower for word in ['track my order', 'where is my order', 'track order']):
        return "📦 I can help you track your order!\n\nPlease paste your **Order ID** (e.g., GRO-2026-3150) or type **'my orders'** to see your recent orders."

    # 4. My Orders Intent
    if any(word in message_lower for word in ['my orders', 'recent orders', 'order history', 'list orders']):
        orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
        if orders:
            return "INTENT_MY_ORDERS"
        return "📦 You haven't placed any orders yet!\n\nStart shopping to place your first order and see it here. 🛒"

    # 5. Delivery Help
    if any(word in message_lower for word in ['deliver', 'shipping', 'how long', 'delay', 'late']):
        return "🚚 **Delivery Support**\n\n• Most orders arrive within 10-20 minutes.\n• If your order is delayed, please provide the Order ID.\n• All deliveries are handled by our verified Grodiur partners."

    # 6. Refund / Returns
    if any(word in message_lower for word in ['refund', 'return', 'cancel', 'wrong item', 'missing']):
        return "↩️ **Refund & Returns**\n\n• For missing or wrong items, please report within 2 hours of delivery.\n• Fresh items are non-returnable but eligible for refund if damaged.\n• Refunds are usually processed within 24 hours to your original payment method."

    # 7. Help menu
    if any(word in message_lower for word in ['help', 'what can you', 'options']):
        return "🤖 **I can help you with:**\n\n• **Track Order** (paste Order ID)\n• **My Orders** (view history)\n• **Search Products** (type any product name)\n• **Delivery Support**\n• **Refunds & Returns**\n\nJust type what you need!"

    # 8. Product Search Intent — check if message could be a product name
    # Skip very short single-char messages and common non-product words
    skip_words = {'a', 'an', 'the', 'is', 'it', 'ok', 'no', 'yes', 'ya', 'ye', 'yep',
                  'thanks', 'thank', 'bye', 'good', 'bad', 'nice', 'great', 'hmm', 'hm',
                  'what', 'how', 'why', 'when', 'who', 'which', 'can', 'do', 'did'}
    
    # Extract the actual search query (strip natural language prefixes)
    search_query = message_lower
    for prefix in ['show me ', 'show ', 'find ', 'search ', 'search for ', 'i want ', 
                    'i need ', 'need ', 'get me ', 'get ', 'buy ', 'looking for ', 'look for ']:
        if search_query.startswith(prefix):
            search_query = search_query[len(prefix):].strip()
            break

    if search_query and search_query not in skip_words and len(search_query) >= 2:
        return f"INTENT_PRODUCT_SEARCH|{search_query}"

    # Default
    return "I'm not sure about that 🤔\n\nYou can type **'track order'**, **'my orders'**, a **product name**, or **'refund'** for help. 🛒"


@csrf_exempt
@login_required
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')
        response = get_bot_response(message, request.user)
        return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request'})