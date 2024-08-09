# admin_panel/views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, OuterRef, Subquery, IntegerField, DecimalField
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.db.models.functions import TruncMonth
from admin_panel.models import CustomUser
from shop.models import Product, Category
from service.models import ServiceRequest
from orders.models import Order, OrderItem
from .forms import ProductForm, OrderUpdateForm, ServiceRequestForm, CustomUserCreationForm, UserEditForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from chat.models import ChatSession, ChatMessage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import CategoryForm
import json


User = get_user_model()

def superadmin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.session.get('user_type') == 'superadmin':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_superadmin() or request.user.is_admin()):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper

class SuperAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superadmin()

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('admin_panel:dashboard')

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_superadmin() or self.request.user.is_admin())

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('admin_panel:admin_login')



@superadmin_required
def user_management(request):
    users = CustomUser.objects.all()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = form.cleaned_data['user_type']
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'User created successfully.')
            return redirect('admin_panel:user_management')
    else:
        form = CustomUserCreationForm()
    return render(request, 'admin_panel/user_management.html', {'users': users, 'form': form})


@superadmin_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('admin_panel:user_management')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'admin_panel/edit_user.html', {'form': form, 'user': user})

@user_passes_test(lambda u: u.is_staff)
def admin_chat_list(request):
    active_sessions = ChatSession.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'admin_panel/chat_list.html', {'active_sessions': active_sessions})

@user_passes_test(lambda u: u.is_staff)
def admin_chat_detail(request, session_id):
    chat_session = get_object_or_404(ChatSession, id=session_id)
    messages = ChatMessage.objects.filter(user=chat_session.user).order_by('timestamp')
    return render(request, 'admin_panel/chat_detail.html', {'chat_session': chat_session, 'messages': messages})

@csrf_exempt
@user_passes_test(lambda u: u.is_staff)
def admin_send_message(request, session_id):
    if request.method == 'POST':
        chat_session = get_object_or_404(ChatSession, id=session_id)
        data = json.loads(request.body)
        message = data.get('message')
        if message:
            chat_message = ChatMessage.objects.create(user=chat_session.user, admin=request.user, message=message, is_admin=True)
            return JsonResponse({'status': 'success', 'message': chat_message.message})
    return JsonResponse({'status': 'error'})

@user_passes_test(lambda u: u.is_staff)
def admin_get_messages(request, session_id):
    chat_session = get_object_or_404(ChatSession, id=session_id)
    messages = ChatMessage.objects.filter(user=chat_session.user).order_by('timestamp')
    return JsonResponse({'messages': list(messages.values())})

@admin_required
def admin_dashboard(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_revenue = OrderItem.objects.aggregate(Sum('price'))['price__sum'] or 0
    total_service_requests = ServiceRequest.objects.count()
    total_customers = User.objects.filter(is_staff=False).count()
    new_customers_last_30_days = User.objects.filter(
        is_staff=False, date_joined__gte=timezone.now() - timedelta(days=30)).count()
    
    # Calculate revenue growth
    revenue_growth = 0
    last_order = Order.objects.last()
    if last_order:
        thirty_days_ago = last_order.created - timedelta(days=30)
        previous_revenue = OrderItem.objects.filter(order__created__lt=thirty_days_ago).aggregate(
            Sum('price'))['price__sum'] or 0
        if previous_revenue > 0:
            revenue_growth = ((total_revenue - previous_revenue) / previous_revenue) * 100
        elif total_revenue > 0:
            revenue_growth = 100  # If there was no previous revenue but there is current revenue, growth is 100%

    product_categories = Category.objects.all()
    recent_orders = Order.objects.order_by('-created')[:5]
    recent_service_requests = ServiceRequest.objects.order_by('-created_at')[:5]

    top_selling_product = Product.objects.annotate(
        total_sold=Sum('order_items_shop__quantity')
    ).order_by('-total_sold').first()

    # Prepare data for the Kenya map
    order_locations = Order.objects.values('city').annotate(count=Count('id'))
    
    # You might need to map city names to coordinates
    # This is a simplified example, you'd need a more comprehensive mapping
    city_coordinates = {
        'Nairobi': [36.8219, -1.2921],
        'Mombasa': [39.6682, -4.0435],
        'Kisumu': [34.7617, -0.0917],
        'Nakuru': [36.0667, -0.3031],
        'Eldoret': [35.2699, 0.5200],
        # Add more cities and their coordinates as needed
    }
    
    orders_with_coordinates = [
        {
            'name': order['city'],
            'count': order['count'],
            'coordinates': city_coordinates.get(order['city'], [0, 0])  # Default to [0, 0] if city not found
        }
        for order in order_locations
    ]

    active_chat_sessions = ChatSession.objects.filter(is_active=True).order_by('-created_at')[:5]

    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_service_requests': total_service_requests,
        'revenue_growth': round(revenue_growth, 2),
        'product_categories': product_categories,
        'recent_orders': recent_orders,
        'recent_service_requests': recent_service_requests,
        'total_customers': total_customers,
        'new_customers_last_30_days': new_customers_last_30_days,
        'top_selling_product': top_selling_product,
        'orders_with_coordinates': orders_with_coordinates,
        'active_chat_sessions': active_chat_sessions,
    }
    return render(request, 'admin_panel/dashboard.html', context)

@superadmin_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully.')
            return redirect('admin_panel:category_list')
    else:
        form = CategoryForm()
    return render(request, 'admin_panel/category_form.html', {'form': form, 'title': 'Add Category'})

@method_decorator(superadmin_required, name='dispatch')
class CategoryListView(SuperAdminRequiredMixin, ListView):
    model = Category
    template_name = 'admin_panel/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10

@method_decorator(superadmin_required, name='dispatch')
class CategoryUpdateView(SuperAdminRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'admin_panel/category_form.html'
    success_url = reverse_lazy('admin_panel:category_list')

    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully.')
        return super().form_valid(form)

@method_decorator(superadmin_required, name='dispatch')
class CategoryDeleteView(SuperAdminRequiredMixin, DeleteView):
    model = Category
    template_name = 'admin_panel/category_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:category_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Category deleted successfully.')
        return super().delete(request, *args, **kwargs)

@method_decorator(admin_required, name='dispatch')
class ProductListView(AdminRequiredMixin, ListView):
    model = Product
    template_name = 'admin_panel/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

@method_decorator(superadmin_required, name='dispatch')
class ProductCreateView(SuperAdminRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'admin_panel/product_form.html'
    success_url = reverse_lazy('admin_panel:product_list')

    def form_valid(self, form):
        messages.success(self.request, 'Product created successfully.')
        return super().form_valid(form)

@method_decorator(superadmin_required, name='dispatch')
class ProductUpdateView(SuperAdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'admin_panel/product_form.html'
    success_url = reverse_lazy('admin_panel:product_list')

    def form_valid(self, form):
        messages.success(self.request, 'Product updated successfully.')
        return super().form_valid(form)

@method_decorator(superadmin_required, name='dispatch')
class ProductDeleteView(SuperAdminRequiredMixin, DeleteView):
    model = Product
    template_name = 'admin_panel/product_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:product_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Product deleted successfully.')
        return super().delete(request, *args, **kwargs)

@method_decorator(admin_required, name='dispatch')
class OrderListView(AdminRequiredMixin, ListView):
    model = Order
    template_name = 'admin_panel/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.all().order_by('-created')

@method_decorator(admin_required, name='dispatch')
class OrderDetailView(AdminRequiredMixin, DetailView):
    model = Order
    template_name = 'admin_panel/order_detail.html'
    context_object_name = 'order'

@method_decorator(superadmin_required, name='dispatch')
class OrderUpdateView(SuperAdminRequiredMixin, UpdateView):
    model = Order
    form_class = OrderUpdateForm
    template_name = 'admin_panel/order_form.html'
    success_url = reverse_lazy('admin_panel:order_list')

    def form_valid(self, form):
        messages.success(self.request, 'Order updated successfully.')
        return super().form_valid(form)

@method_decorator(superadmin_required, name='dispatch')
class OrderDeleteView(SuperAdminRequiredMixin, DeleteView):
    model = Order
    template_name = 'admin_panel/order_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:order_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Order deleted successfully.')
        return super().delete(request, *args, **kwargs)

@method_decorator(admin_required, name='dispatch')
class ServiceRequestListView(AdminRequiredMixin, ListView):
    model = ServiceRequest
    template_name = 'admin_panel/service_request_list.html'
    context_object_name = 'service_requests'
    paginate_by = 10

    def get_queryset(self):
        return ServiceRequest.objects.all().order_by('-created_at')

@method_decorator(admin_required, name='dispatch')
class ServiceRequestDetailView(AdminRequiredMixin, DetailView):
    model = ServiceRequest
    template_name = 'admin_panel/service_request_detail.html'
    context_object_name = 'service_request'

@method_decorator(admin_required, name='dispatch')
class ServiceRequestUpdateView(AdminRequiredMixin, UpdateView):
    model = ServiceRequest
    form_class = ServiceRequestForm
    template_name = 'admin_panel/service_request_form.html'
    success_url = reverse_lazy('admin_panel:service_request_list')

    def form_valid(self, form):
        messages.success(self.request, 'Service request updated successfully.')
        return super().form_valid(form)

@method_decorator(superadmin_required, name='dispatch')
class ServiceRequestDeleteView(SuperAdminRequiredMixin, DeleteView):
    model = ServiceRequest
    template_name = 'admin_panel/service_request_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:service_request_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Service request deleted successfully.')
        return super().delete(request, *args, **kwargs)

@method_decorator(admin_required, name='dispatch')
class CustomerListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'admin_panel/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 10

    def get_queryset(self):
        # Subquery to get the count of orders for each user
        order_count_subquery = Order.objects.filter(
            email=OuterRef('email')
        ).values('email').annotate(
            order_count=Count('id')
        ).values('order_count')

        # Subquery to get the total spent by each user
        total_spent_subquery = OrderItem.objects.filter(
            order__email=OuterRef('email')
        ).values('order__email').annotate(
            total_spent=Sum('price')
        ).values('total_spent')

        return User.objects.filter(is_staff=False).annotate(
            order_count=Subquery(order_count_subquery, output_field=IntegerField()),
            total_spent=Subquery(total_spent_subquery, output_field=DecimalField(max_digits=10, decimal_places=2))
        ).order_by('-date_joined')

@method_decorator(admin_required, name='dispatch')
class CustomerDetailView(AdminRequiredMixin, DetailView):
    model = User
    template_name = 'admin_panel/customer_detail.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        context['orders'] = Order.objects.filter(user=customer).order_by('-created')[:5]
        context['service_requests'] = ServiceRequest.objects.filter(user=customer).order_by('-created_at')[:5]
        return context

@admin_required
def reports(request):
    # Sales over time
    sales_over_time = OrderItem.objects.annotate(month=TruncMonth('order__created')).values('month').annotate(
        total_sales=Sum('price'),
        order_count=Count('order', distinct=True)
    ).order_by('month')

    # Top selling products
    top_products = Product.objects.annotate(
        total_sold=Sum('order_items_shop__quantity'),
        revenue=Sum('order_items_shop__price')
    ).order_by('-total_sold')[:10]

    # Service request statistics
    service_stats = ServiceRequest.objects.values('status').annotate(count=Count('id'))

    context = {
        'sales_over_time': list(sales_over_time),
        'top_products': top_products,
        'service_stats': service_stats,
    }
    return render(request, 'admin_panel/reports.html', context)

@admin_required
def order_map(request):
    # Aggregate orders by city
    order_locations = Order.objects.values('city').annotate(count=Count('id'))

    # City coordinates (you should expand this with more Kenyan cities)
    city_coordinates = {
        'Nairobi': [36.8219, -1.2921],
        'Mombasa': [39.6682, -4.0435],
        'Kisumu': [34.7617, -0.0917],
        'Nakuru': [36.0667, -0.3031],
        'Eldoret': [35.2699, 0.5200],
        # Add more cities and their coordinates as needed
    }

    orders_with_coordinates = [
        {
            'name': location['city'],
            'count': location['count'],
            'coordinates': city_coordinates.get(location['city'], [0, 0])
        }
        for location in order_locations
    ]

    # Calculate additional statistics
    total_cities = order_locations.count()
    total_orders = sum(location['count'] for location in order_locations)
    avg_orders_per_city = total_orders / total_cities if total_cities > 0 else 0

    # Get top 5 cities by order count
    top_cities = sorted(order_locations, key=lambda x: x['count'], reverse=True)[:5]

    context = {
        'orders_with_coordinates': orders_with_coordinates,
        'top_cities': top_cities,
        'total_cities': total_cities,
        'total_orders': total_orders,
        'avg_orders_per_city': avg_orders_per_city,
    }
    print("Debug - orders_with_coordinates:", orders_with_coordinates)  # Add this line for debugging
    return render(request, 'admin_panel/order_map.html', context)

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and (user.is_superadmin() or user.is_admin()):
                login(request, user)
                # Update session with user type
                request.session['user_type'] = 'superadmin' if user.is_superadmin() else 'admin'
                return redirect('admin_panel:dashboard')
            else:
                messages.error(request, "Invalid username or password, or insufficient permissions.")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, 'admin_panel/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('admin_panel:admin_login')