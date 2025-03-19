from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<uuid:pk>/', views.product_detail, name='product_detail'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/<uuid:pk>/edit/', views.edit_product, name='edit_product'),
    path('products/<uuid:pk>/delete/', views.delete_product, name='delete_product'),
    path('products/<uuid:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('products/<uuid:pk>/report/', views.report_product, name='report_product'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
] 