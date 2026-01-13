from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from .models import Search

# Create your views here.

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    #Search.objects.create(search = search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url, headers=headers, proxies={})
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('li', {'class': "cl-static-search-result"})
    
    final_postings = []

    for post in post_listings:
        post_title = post.get('title')
        post_url = post.find('a').get('href')
        if post.find(class_='price'):
            post_price = post.find(class_='price').text
        else:
            post_price = 'N/A'
        post_image_url = "https://craigslist.org/images/peace.jpg"
        final_postings.append((post_title, post_url, post_price, post_image_url))
    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings
    }
    return render(request, "my_app/new_search.html", stuff_for_frontend)
