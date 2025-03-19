from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
import uuid
from products.models import Product
from .models import Order, Payment
from .forms import OrderForm, PaymentForm

@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # Check if product is available
    if product.status != 'available':
        messages.error(request, 'This product is no longer available!')
        return redirect('product_detail', pk=product_id)
    
    # Prevent buying own product
    if request.user == product.seller:
        messages.error(request, 'You cannot buy your own product!')
        return redirect('product_detail', pk=product_id)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.buyer = request.user
            order.product = product
            order.total_price = product.price
            order.save()
            
            # Update product status
            product.status = 'reserved'
            product.save()
            
            messages.success(request, 'Your order has been created! Proceed to payment.')
            return redirect('payment', order_id=order.id)
    else:
        form = OrderForm()
    
    context = {
        'form': form,
        'product': product,
    }
    
    return render(request, 'orders/create_order.html', context)

@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    
    # Check if the user is the buyer
    if request.user != order.buyer:
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    # Check if payment already exists
    existing_payment = Payment.objects.filter(order=order).first()
    if existing_payment and existing_payment.status == 'completed':
        messages.info(request, 'Payment has already been completed for this order.')
        return redirect('order_detail', order_id=order.id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=existing_payment)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            payment.amount = order.total_price
            payment.transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
            payment.status = 'completed'
            payment.save()
            
            # Update order status
            order.status = 'processing'
            order.save()
            
            # Update product status
            order.product.status = 'sold'
            order.product.save()
            
            messages.success(request, 'Payment successful! Your order is now being processed.')
            return redirect('order_detail', order_id=order.id)
    else:
        form = PaymentForm(instance=existing_payment)
    
    context = {
        'form': form,
        'order': order,
    }
    
    return render(request, 'orders/payment.html', context)

@login_required
def order_list(request):
    # Get orders where the user is either the buyer or the seller
    buyer_orders = Order.objects.filter(buyer=request.user)
    seller_orders = Order.objects.filter(product__seller=request.user)
    
    context = {
        'buyer_orders': buyer_orders,
        'seller_orders': seller_orders,
    }
    
    return render(request, 'orders/order_list.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    
    # Check if the user is either the buyer or the seller
    if request.user != order.buyer and request.user != order.product.seller:
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    context = {
        'order': order,
    }
    
    return render(request, 'orders/order_detail.html', context)

@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    
    # Check if the user is the seller
    if request.user != order.product.seller:
        return HttpResponseForbidden("You are not authorized to update this order.")
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [status[0] for status in Order.STATUS_CHOICES]:
            order.status = new_status
            order.updated_at = timezone.now()
            order.save()
            messages.success(request, f'Order status updated to {new_status}!')
        else:
            messages.error(request, 'Invalid status!')
    
    return redirect('order_detail', order_id=order.id)

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    
    # Check if the user is the buyer
    if request.user != order.buyer:
        return HttpResponseForbidden("You are not authorized to cancel this order.")
    
    # Check if the order can be cancelled
    if order.status in ['delivered', 'completed']:
        messages.error(request, 'This order cannot be cancelled!')
        return redirect('order_detail', order_id=order.id)
    
    if request.method == 'POST':
        order.status = 'cancelled'
        order.updated_at = timezone.now()
        order.save()
        
        # Update product status back to available
        order.product.status = 'available'
        order.product.save()
        
        # Handle payment refund if needed
        payment = Payment.objects.filter(order=order, status='completed').first()
        if payment:
            payment.status = 'refunded'
            payment.save()
        
        messages.success(request, 'Your order has been cancelled!')
        return redirect('order_list')
    
    return render(request, 'orders/cancel_order.html', {'order': order}) 