from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('start/', views.start_conversation, name='start_conversation'),
    path('start/user/<int:user_id>/', views.start_conversation, name='start_conversation_with_user'),
    path('start/product/<uuid:product_id>/', views.start_conversation, name='start_conversation_about_product'),
    path('delete/<int:conversation_id>/', views.delete_conversation, name='delete_conversation'),
] 