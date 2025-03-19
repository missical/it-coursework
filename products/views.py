from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, Category, ProductImage, Favorite, Report
from .forms import ProductForm, ProductImageFormSet, ProductSearchForm, ReportForm

def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(status='available').order_by('-created_at')[:6]
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    
    return render(request, 'products/home.html', context)

def product_list(request):
    form = ProductSearchForm(request.GET)
    products = Product.objects.filter(status='available')
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        location = form.cleaned_data.get('location')
        
        if query:
            products = products.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query)
            )
        
        if category:
            products = products.filter(category=category)
        
        if min_price:
            products = products.filter(price__gte=min_price)
        
        if max_price:
            products = products.filter(price__lte=max_price)
        
        if location:
            products = products.filter(location__icontains=location)
    
    context = {
        'products': products,
        'form': form,
        'categories': Category.objects.all(),
    }
    
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    is_favorited = False
    
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, product=product).exists()
    
    context = {
        'product': product,
        'is_favorited': is_favorited,
    }
    
    return render(request, 'products/product_detail.html', context)

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, status='available')
    
    context = {
        'category': category,
        'products': products,
    }
    
    return render(request, 'products/category_products.html', context)

@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        formset = ProductImageFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            
            # Save product images
            instances = formset.save(commit=False)
            for instance in instances:
                instance.product = product
                instance.save()
            
            messages.success(request, 'Your product has been listed!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
        formset = ProductImageFormSet()
    
    context = {
        'form': form,
        'formset': formset,
    }
    
    return render(request, 'products/create_product.html', context)

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Check if the user is the seller
    if request.user != product.seller:
        messages.error(request, 'You are not authorized to edit this product!')
        return redirect('product_detail', pk=product.pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Your product has been updated!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)
    
    context = {
        'form': form,
        'formset': formset,
        'product': product,
    }
    
    return render(request, 'products/edit_product.html', context)

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Check if the user is the seller
    if request.user != product.seller:
        messages.error(request, 'You are not authorized to delete this product!')
        return redirect('product_detail', pk=product.pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Your product has been deleted!')
        return redirect('dashboard')
    
    return render(request, 'products/delete_product.html', {'product': product})

@login_required
def toggle_favorite(request, pk):
    product = get_object_or_404(Product, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        favorite.delete()
        is_favorited = False
    else:
        is_favorited = True
    
    # 判断是否是AJAX请求
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorited': is_favorited})
    
    return redirect('product_detail', pk=product.pk)

@login_required
def report_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.product = product
            report.reporter = request.user
            report.save()
            messages.success(request, 'Your report has been submitted!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ReportForm()
    
    context = {
        'form': form,
        'product': product,
    }
    
    return render(request, 'products/report_product.html', context) 