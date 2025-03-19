from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, RatingForm
from .models import Rating
from products.models import Product, Favorite

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request, 'users/profile.html', context)

@login_required
def dashboard(request):
    user_products = Product.objects.filter(seller=request.user)
    user_favorites = Favorite.objects.filter(user=request.user)
    user_ratings = Rating.objects.filter(user=request.user)
    
    avg_rating = 0
    if user_ratings.exists():
        avg_rating = sum(rating.rating for rating in user_ratings) / user_ratings.count()
    
    context = {
        'products': user_products,
        'favorites': user_favorites,
        'ratings': user_ratings,
        'avg_rating': avg_rating
    }
    
    return render(request, 'users/dashboard.html', context)

def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    user_products = Product.objects.filter(seller=user)
    user_ratings = Rating.objects.filter(user=user)
    
    avg_rating = 0
    if user_ratings.exists():
        avg_rating = sum(rating.rating for rating in user_ratings) / user_ratings.count()
    
    # Check if the current user has already rated this user
    user_rated = False
    if request.user.is_authenticated:
        user_rated = Rating.objects.filter(user=user, rater=request.user).exists()
    
    context = {
        'profile_user': user,
        'products': user_products,
        'ratings': user_ratings,
        'avg_rating': avg_rating,
        'user_rated': user_rated
    }
    
    return render(request, 'users/user_detail.html', context)

@login_required
def rate_user(request, username):
    user = get_object_or_404(User, username=username)
    
    # Prevent users from rating themselves
    if request.user == user:
        messages.error(request, 'You cannot rate yourself!')
        return redirect('user_detail', username=username)
    
    # Check if the user has already rated this user
    existing_rating = Rating.objects.filter(user=user, rater=request.user).first()
    
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=existing_rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = user
            rating.rater = request.user
            rating.save()
            messages.success(request, f'Your rating for {username} has been submitted!')
            return redirect('user_detail', username=username)
    else:
        form = RatingForm(instance=existing_rating)
    
    return render(request, 'users/rate_user.html', {'form': form, 'rated_user': user})
