from django.shortcuts import render, get_object_or_404
from .models import Product, Customer, Order, OrderItem, Restaurant

def home_page(request):
    restaurants = Restaurant.objects.prefetch_related('products').all()
    return render(request, 'home.html', {'restaurants': restaurants})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, product_slug=slug)
    return render(request, 'product_detail.html', {'product': product})

def create_order(request):
    if request.method == 'POST':
        # Example logic for creating an order
        customer_id = request.POST['customer_id']
        product_ids = request.POST.getlist('product_ids')
        quantities = request.POST.getlist('quantities')
        
        customer = get_object_or_404(Customer, pk=customer_id)
        order = Order.objects.create(customer=customer, total_price=0)
        
        total_price = 0
        for product_id, quantity in zip(product_ids, quantities):
            product = get_object_or_404(Product, pk=product_id)
            price = product.product_price * int(quantity)
            total_price += price
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
        
        order.total_price = total_price
        order.save()
        return render(request, 'order_success.html', {'order': order})
    
    customers = Customer.objects.all()
    products = Product.objects.all()
    return render(request, 'create_order.html', {'customers': customers, 'products': products})

