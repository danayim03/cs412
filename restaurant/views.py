from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
import time

# Create your views here.

def main_page(request):
    return render(request, 'restaurant/main.html')

def order_page(request):
    daily_specials = {
        'KBBQ': 12,
        'Sweet chili chicken': 11,
        'Garlic chicken': 10,
        'Jokbal': 14,
        'Hot dog': 8
    }

    daily_special, special_price = random.choice(list(daily_specials.items()))
    
    context = {
        'daily_special': daily_special,
        'special_price': special_price
    }

    return render(request, 'restaurant/order.html', context)

def confirmation_page(request):
    menu_items = {
        'Tteokbokki': 10,
        'Soondae': 8,
        'Gimbap': 7,
        'Dak gangjeong': 7,
        'Twigim': 10
    }

    extra_options = {
        'Extra Cheese': 1
    }

    ordered_items = []
    total_price = 0

    daily_special = request.POST.get('daily_special')
    special_price = float(request.POST.get('special_price', 0))

    if daily_special:
        ordered_items.append(daily_special)
        total_price += special_price

    for item, price in menu_items.items():
        if request.POST.get(item):
            ordered_items.append(item)
            total_price += price

    for option_name, price in extra_options.items():
        if request.POST.get(option_name):
            ordered_items.append("Extra Cheese")
            total_price += price

    current_time = time.time()
    random_minutes = random.randint(30, 60)
    ready_time_seconds = random_minutes * 60
    ready_time = current_time + ready_time_seconds
    ready_time_str = time.strftime('%I:%M %p', time.localtime(ready_time))

    customer_name = request.POST.get('customer_name', 'N/A')
    customer_phone = request.POST.get('customer_phone', 'N/A')
    customer_email = request.POST.get('customer_email', 'N/A')

    context = {
        'ordered_items': ordered_items,
        'total_price': total_price,
        'ready_time': ready_time_str,
        'customer_name': customer_name,
        'customer_phone': customer_phone,
        'customer_email': customer_email,
        'current_time': time.strftime('%a %b %d %H:%M:%S %Y')
    }

    return render(request, 'restaurant/confirmation.html', context)
