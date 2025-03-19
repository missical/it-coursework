from django.urls import path
from . import views

urlpatterns = [
    path('create/<uuid:product_id>/', views.create_order, name='create_order'),
    path('payment/<uuid:order_id>/', views.payment, name='payment'),
    path('list/', views.order_list, name='order_list'),
    path('detail/<uuid:order_id>/', views.order_detail, name='order_detail'),
    path('update-status/<uuid:order_id>/', views.update_order_status, name='update_order_status'),
    path('cancel/<uuid:order_id>/', views.cancel_order, name='cancel_order'),
] 