from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
from django.http import JsonResponse

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from Home.models import Product
from .models import Cart, CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('products')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})

@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()
    return redirect('view_cart')

@login_required
def adjust_cart(request, item_id):
    cart = Cart.objects.get(user=request.user)  # Obtén el carrito del usuario actual, ajusta esto según tu implementación
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))  # Obtén la nueva cantidad desde el formulario
        if new_quantity > 0:
            item.quantity = new_quantity
            item.save()

    return redirect('view_cart')  # Redirige de vuelta al carrito o a donde sea necesario
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
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error please try again"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})



def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logout"))
    return redirect ('home')

def register_user(request):
    form= SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data ['username']
            password = form.cleaned_data ['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have been register succesfully"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error please try again"))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})
