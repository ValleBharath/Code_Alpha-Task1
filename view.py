from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Product, Order

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def add_to_cart(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)
    cart = request.session.get('cart', [])
    cart.append(product.id)
    request.session['cart'] = cart
    return redirect('product_list')

def checkout(request):
    cart_ids = request.session.get('cart', [])
    products_in_cart = Product.objects.filter(id__in=cart_ids)
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        order = Order.objects.create(name=name, email=email, address=address)
        request.session['cart'] = []  # Empty the cart after order
        return redirect('product_list')

    return render(request, 'store/checkout.html', {'products': products_in_cart})
