#shop/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Product, Cart, CartItem
from cart.forms import CartAddProductForm
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from cart.cart import Cart
import logging



logger = logging.getLogger(__name__)

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        for product in products:
            logger.debug(f"Product: {product.name}, Image URL: {product.get_image_url()}")
    return render(request, 'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    additional_images = product.additional_images.all()
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    cart_product_form = CartAddProductForm()
    
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'related_products': related_products,
        'additional_images': additional_images,
        'additional_info': {
            'Brand': product.brand,
            'Model': product.model,
            'Cooling Capacity': f"{product.cooling_capacity} kW" if product.cooling_capacity else "N/A",
            'Heating Capacity': f"{product.heating_capacity} kW" if product.heating_capacity else "N/A",
            'Energy Efficiency': product.energy_efficiency,
            'Noise Level': f"{product.noise_level} dB" if product.noise_level else "N/A",
            'Warranty': f"{product.warranty} years" if product.warranty else "N/A",
        }
    }
    
    return render(request, 'shop/product/detail.html', context)

def product_image(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.image:
        logger.debug(f"Product {product_id} image size: {len(product.image)} bytes")
        logger.debug(f"Product {product_id} image type: {type(product.image)}")
        logger.debug(f"Product {product_id} image name: {product.image_name}")
        
        # Check if the image data starts with known image format headers
        if product.image.startswith(b'\xff\xd8\xff'):  # JPEG header
            content_type = 'image/jpeg'
        elif product.image.startswith(b'\x89PNG\r\n\x1a\n'):  # PNG header
            content_type = 'image/png'
        else:
            logger.warning(f"Unknown image format for product {product_id}")
            content_type = 'application/octet-stream'
        
        return HttpResponse(product.image, content_type=content_type)
    else:
        logger.warning(f"No image found for product {product_id}")
    raise Http404("Image does not exist")

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['update'])
        
        return JsonResponse({
            'status': 'success',
            'message': f'{product.name} added to cart',
            'cart_total': len(cart)
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid form data'}, status=400)

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')


def cart_detail(request):
    cart = Cart(request)  # This should now work correctly
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'update': True})
    return render(request, 'shop/cart/detail.html', {'cart': cart})

def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        # Process the order
        # Clear the cart
        cart.clear()
        return render(request, 'shop/orders/created.html')
    return render(request, 'shop/orders/create.html', {'cart': cart})

def calculate_shipping(request):
    if request.method == 'POST':
        # Implement shipping calculation logic here
        shipping_cost = 10.00  # Example fixed shipping cost
        return JsonResponse({'shipping_cost': shipping_cost})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def product_search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ).filter(available=True)
    
    return render(request, 'shop/product/list.html', {
        'products': products,
        'query': query
    })

def compare_products(request):
    product_ids = request.GET.get('product_id', '').split(',')
    product_ids = [int(id) for id in product_ids if id.isdigit()]
    products = Product.objects.filter(id__in=product_ids)
    
    comparison_fields = [
        'name', 'brand', 'model', 'price', 'cooling_capacity', 'heating_capacity',
        'energy_efficiency', 'noise_level', 'warranty'
    ]
    
    comparison_data = {field: [] for field in comparison_fields}
    
    for product in products:
        for field in comparison_fields:
            value = getattr(product, field)
            if field == 'price':
                value = f"KES {value:,.2f}"
            elif field in ['cooling_capacity', 'heating_capacity']:
                value = f"{value} kW" if value else "N/A"
            elif field == 'noise_level':
                value = f"{value} dB" if value else "N/A"
            elif field == 'warranty':
                value = f"{value} years" if value else "N/A"
            comparison_data[field].append(value)
    
    return render(request, 'shop/compare_products.html', {
        'products': products,
        'comparison_data': comparison_data
    })
