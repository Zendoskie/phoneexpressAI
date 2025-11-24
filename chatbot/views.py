from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
import requests
from .models import Phone, Order


def index(request):
    """Intro/welcome page"""
    return render(request, 'chatbot/index.html')


def chatbot_view(request):
    """Main chatbot page"""
    return render(request, 'chatbot/chatbot.html')


def phones_api(request):
    """API endpoint to get list of available phones"""
    phones = Phone.objects.filter(is_available=True, stock__gt=0)
    phone_list = []
    for phone in phones:
        phone_list.append({
            'id': phone.id,
            'name': phone.name,
            'brand': phone.brand,
            'model': phone.model,
            'price_php': float(phone.price_php),
            'description': phone.description,
            'stock': phone.stock,
        })
    return JsonResponse({'phones': phone_list})


@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    """API endpoint to handle chatbot messages using OpenRouter"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        if not user_message:
            return JsonResponse({
                'response': 'Please provide a message.',
                'success': False
            }, status=400)
        
        # Get available phones for context
        try:
            phones = Phone.objects.filter(is_available=True, stock__gt=0)
            phones_context = "\n".join([
                f"- {p.brand} {p.model}: ₱{p.price_php:,.2f} ({p.stock} in stock) - {p.description}"
                for p in phones
            ])
            if not phones_context:
                phones_context = "No phones are currently available in stock."
        except Exception as e:
            phones_context = "Phone database is currently unavailable."
            print(f"Error fetching phones: {e}")
        
        # System prompt for the AI assistant - Phone focused only
        system_prompt = f"""You are a phone specialist AI assistant for Phone Express AI. Your ONLY focus is helping customers with phones.

Your role is EXCLUSIVELY about phones:
1. Help customers find the perfect phone based on their needs, budget, and preferences
2. Provide detailed information about phone specifications, features, and capabilities
3. Compare different phone models and brands
4. Answer questions about phone prices, availability, and ordering
5. Recommend phones based on specific requirements (camera quality, battery life, performance, etc.)

Available phones:
{phones_context}

IMPORTANT RULES:
- You ONLY discuss phones and phone-related topics
- If asked about non-phone topics, politely redirect to phone-related questions
- All prices are in Philippine Peso (PHP/₱)
- Always mention prices in PHP format (e.g., ₱25,999.00)
- Be friendly, professional, and knowledgeable about phones
- If a customer wants to order a phone, guide them to provide: name, email, phone number, shipping address, and which phone they want
- Focus on phone specifications, features, comparisons, and recommendations
- Check stock availability before confirming orders

Stay focused on phones only. Current conversation context is maintained through the chat history."""
        
        # Prepare the request to OpenRouter API
        openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        
        # Get chat history if available
        chat_history = data.get('history', [])
        
        # Build messages for the API
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add chat history (last 10 messages to avoid token limits)
        for msg in chat_history[-10:]:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 500,
        }
        
        # Make request to OpenRouter
        response = requests.post(openrouter_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        # Check if we got a valid response
        if 'choices' not in result or len(result['choices']) == 0:
            return JsonResponse({
                'response': 'Sorry, I received an invalid response from the AI service. Please try again.',
                'success': False
            }, status=500)
        
        ai_message = result['choices'][0]['message']['content']
        
        return JsonResponse({
            'response': ai_message,
            'success': True
        })
        
    except requests.RequestException as e:
        error_msg = str(e)
        print(f"OpenRouter API Error: {error_msg}")
        # Try to get more details from the response
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                print(f"Error details: {error_detail}")
            except:
                pass
        
        return JsonResponse({
            'response': 'Sorry, I encountered an error connecting to the AI service. Please try again.',
            'success': False,
            'error': error_msg
        }, status=500)
    except KeyError as e:
        print(f"KeyError in chat_api: {e}")
        return JsonResponse({
            'response': 'Sorry, there was an error processing the response. Please try again.',
            'success': False,
            'error': f'Missing key: {str(e)}'
        }, status=500)
    except Exception as e:
        error_msg = str(e)
        print(f"Unexpected error in chat_api: {error_msg}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'response': 'Sorry, something went wrong. Please try again.',
            'success': False,
            'error': error_msg
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    """API endpoint to create a new order"""
    try:
        data = json.loads(request.body)
        
        phone_id = data.get('phone_id')
        quantity = int(data.get('quantity', 1))
        customer_name = data.get('customer_name')
        customer_email = data.get('customer_email')
        customer_phone = data.get('customer_phone')
        shipping_address = data.get('shipping_address')
        
        # Validate required fields
        if not all([phone_id, customer_name, customer_email, customer_phone, shipping_address]):
            return JsonResponse({
                'success': False,
                'message': 'All fields are required'
            }, status=400)
        
        # Get phone
        try:
            phone = Phone.objects.get(id=phone_id, is_available=True)
        except Phone.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Phone not found or not available'
            }, status=404)
        
        # Check stock
        if phone.stock < quantity:
            return JsonResponse({
                'success': False,
                'message': f'Only {phone.stock} units available in stock'
            }, status=400)
        
        # Calculate total price
        total_price = phone.price_php * quantity
        
        # Create order
        order = Order.objects.create(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            phone=phone,
            quantity=quantity,
            total_price_php=total_price,
            shipping_address=shipping_address,
            status='pending'
        )
        
        # Update stock
        phone.stock -= quantity
        if phone.stock == 0:
            phone.is_available = False
        phone.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Order placed successfully!',
            'order_id': order.id,
            'total_price_php': float(total_price)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error creating order: {str(e)}'
        }, status=500)

