#service/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Equipment, EquipmentCategory, ServiceRequest
from .forms import ServiceRequestForm
from shop.models import Product
from shop.models import Product, Category 

def service_request(request):
    initial_data = {}
    product = None
    product_id = request.GET.get('product_id')
    
    if product_id:
        product = get_object_or_404(Product, id=product_id)
        initial_data['product'] = product
        initial_data['description'] = f"Installation request for {product.name}"

    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.save()
            form.save_m2m()
            return redirect('service:request_confirmation')
    else:
        form = ServiceRequestForm(initial=initial_data)

    equipment_categories = EquipmentCategory.objects.all()
    product_categories = Category.objects.all()

    context = {
        'form': form,
        'equipment_categories': equipment_categories,
        'product_categories': product_categories,
        'product': product,
    }
    return render(request, 'service/service_request.html', context)

def request_confirmation(request):
    return render(request, 'service/request_confirmation.html')

def equipment_list(request):
    equipment = Equipment.objects.all()
    return render(request, 'service/equipment_list.html', {'equipment': equipment})

@login_required
def service_history(request):
    service_requests = ServiceRequest.objects.filter(user=request.user)
    return render(request, 'service/service_history.html', {'service_requests': service_requests})

def request_detail(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    return render(request, 'service/request_detail.html', {'service_request': service_request})