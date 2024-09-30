# quotes/views.py
from django.shortcuts import render
from django.http import HttpResponse
import random

# Sample data for quotes and images
quotes = [
    "You have to trust in something, your gut, destiny, life, karma, whatever.",
    "If you live each day as if it was your last, someday you'll most certainly be right.",
    "The people who are crazy enough to think they can chagne the world, are the ones who do.",
]

images = [
    "https://dreamwalk.com.au/wp-content/uploads/2020/03/Steve-Jobs-trust-in-somthing-quote.jpg",
    "https://dreamwalk.com.au/wp-content/uploads/2020/03/Steve-Jobs-live-each-day-quote.jpg",
    "https://dreamwalk.com.au/wp-content/uploads/2020/03/Steve-Jobs-go-invent-tomorrow-quote.jpg",
]

def main_page(request):
    quote = random.choice(quotes)
    image = random.choice(images)
    return render(request, 'quotes/quote.html', {'quote': quote, 'image': image})

def random_quote(request):
    quote = random.choice(quotes)
    image = random.choice(images)
    return render(request, 'quotes/quote.html', {'quote': quote, 'image': image})

def show_all(request):
    return render(request, 'quotes/show_all.html', {'quotes': quotes, 'images': images})

# quotes/views.py

# About page view
def about(request):
    famous_person_info = {
        "name": "Steve Jobs",  # Replace with the famous person you're showcasing
        "bio": "American businessman, inventor, and investor best known for co-founding the technology company Apple Inc.",
    }
    return render(request, 'quotes/about.html', famous_person_info)

