from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Equipment, EquipmentCategory, ServiceRequest
from .forms import ServiceRequestForm

def service_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.save()
            form.save_m2m()  # Save many-to-many data
            return redirect('service:request_confirmation')
    else:
        form = ServiceRequestForm()
    
    equipment_categories = EquipmentCategory.objects.all()
    return render(request, 'service/service_request.html', {
        'form': form,
        'equipment_categories': equipment_categories
    })

def request_confirmation(request):
    return render(request, 'service/request_confirmation.html')

def equipment_list(request):
    equipment = Equipment.objects.all()
    return render(request, 'service/equipment_list.html', {'equipment': equipment})

@login_required
def service_history(request):
    service_requests = ServiceRequest.objects.filter(user=request.user)
    return render(request, 'service/service_history.html', {'service_requests': service_requests})