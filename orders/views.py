from django.shortcuts import render, redirect
from .forms import OrderCreateForm
from cart.cart import Cart
from .models import OrderItem
from django.http import JsonResponse
from django.views.decorators.http import require_POST


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})

@require_POST
def calculate_shipping(request):
    postal_code = request.POST.get('postal_code')
    city = request.POST.get('city')
    
    # Implement your shipping calculation logic here
    # This is just a placeholder
    shipping_cost = 10.00  # Example fixed shipping cost
    
    return JsonResponse({'shipping_cost': shipping_cost})