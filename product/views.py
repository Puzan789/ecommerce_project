
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from .forms import CartAddProductForm ,SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages

# Create your views here.
def index(request):
    products = Product.objects.all()[1:4]
    

    return render(request,'index.html',{'products': products,})

def About(request):
    return render(request,'About.html')

def Contact(request):
    return render(request,'Contact.html')

def Shop(request):
    products = Product.objects.all()
    return render(request, 'Shop.html', {'products': products})

@login_required
def cart(request):
    order, created = Order.objects.get_or_create(user=request.user, completed=False)
    total_with_extra = order.get_total() + 45  # Precompute the total with the extra value
    context = {
        'order': order,
        'total_with_extra': total_with_extra
    }
    return render(request, 'cart.html', context)
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, completed=False)
    
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product, defaults={'price': product.price})
    
    if not created:
        order_item.quantity += 1
        order_item.save()
    
    return redirect('cart')
@login_required
def remove_from_cart(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)
    order_item.delete()
    return redirect('cart')
@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            item.quantity += 1
        elif action == 'decrease' and item.quantity > 1:
            item.quantity -= 1
        item.save()
    return redirect('cart')
# @login_required
# def checkout(request):
#     order = get_object_or_404(Order, user=request.user, completed=False)
#     if request.method == 'POST':
#         order.completed = True
#         order.save()
#         # Create a new empty order for the user
#         Order.objects.create(user=request.user)
#         return redirect('success')  # Redirect to a success page after checkout
#     context = {'order': order}
    # return render(request, 'checkout.html', context)
@login_required
def checkout(request):
    order = get_object_or_404(Order, user=request.user, completed=False)
    
    if request.method == 'POST':
        # Mark the order as completed
        order.completed = True
        order.save()
        
        # Clear the cart (delete all items from the order)
        order.items.all().delete()
        
        # Create a new empty order for the user
        Order.objects.create(user=request.user)
        
        
        return redirect('success')  # Redirect to a success page after checkout
    
    context = {'order': order}
    return render(request, 'checkout.html', context)


def success(request):
    return render(request, 'success.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def error_404_view(request, exception):
    return render(request, 'errors/404.html', status=404)

def error_500_view(request):
    return render(request, 'errors/500.html', status=500)
# search 
