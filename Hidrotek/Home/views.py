from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, 'home.html', {})

def products(request, category_name=None):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'default')

    if category_name:
        current_category = get_object_or_404(Category, name=category_name)
        items = Product.objects.filter(category=current_category)
    else:
        current_category = None
        items = Product.objects.all()

    if query:
        items = items.filter(name__icontains=query)

    if sort == 'price_low_high':
        items = items.order_by('price')
    elif sort == 'price_high_low':
        items = items.order_by('-price')
    elif sort == 'newest':
        items = items.order_by('-id')
    else:
        items = items.order_by('name')

    paginator = Paginator(items, 12)  # 12 items per page
    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)

    categories = Category.objects.all()
    return render(request, 'products.html', {
        'items': items,
        'categories': categories,
        'total_results': paginator.count,
        'query': query,
        'sort': sort,
    })

def services(request):
    return render(request, 'services.html', {})

def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        query = request.GET.get('q', '')
        sort = request.GET.get('sort', 'default')

        items = Product.objects.filter(category=category)
        
        if query:
            items = items.filter(name__icontains=query)

        if sort == 'price_low_high':
            items = items.order_by('price')
        elif sort == 'price_high_low':
            items = items.order_by('-price')
        elif sort == 'newest':
            items = items.order_by('-id')
        else:
            items = items.order_by('name')

        paginator = Paginator(items, 12)  # 12 items per page
        page_number = request.GET.get('page')
        items = paginator.get_page(page_number)

        categories = Category.objects.all()
        return render(request, 'category.html', {
            'items': items,
            'category': category,
            'categories': categories,
            'total_results': paginator.count,
            'query': query,
            'sort': sort,
        })
    except Category.DoesNotExist:
        messages.error(request, "That category doesn't exist...")
        return redirect('home')
    
def login_user(request):
    return render(request, 'login.html', {})

def logout_user(request):
    return render(request, 'login.html', {})
