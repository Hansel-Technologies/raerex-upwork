#cart/view.py
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.contrib import messages

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
        
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': f'{product.name} added to cart',
                'cart_total': len(cart)
            })
        else:
            messages.success(request, f'{product.name} has been added to your cart.')
            return redirect('cart:cart_detail')
    
    # If the form is not valid
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'error', 'message': 'Invalid form data'}, status=400)
    else:
        messages.error(request, 'Error adding product to cart. Please try again.')
        return redirect('shop:product_list')
    
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})

@require_POST
def cart_update(request):
    cart = Cart(request)
    for key, value in request.POST.items():
        if key.startswith('quantity_'):
            product_id = int(key.split('_')[1])
            product = Product.objects.get(id=product_id)
            cart.add(product=product, quantity=int(value), update_quantity=True)
    return redirect('cart:cart_detail')