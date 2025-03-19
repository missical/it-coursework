from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as django_messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.db.models import Q
from products.models import Product
from .models import Conversation, Message
from .forms import MessageForm, ConversationForm

@login_required
def inbox(request):
    # Get all conversations where the user is a participant
    conversations = Conversation.objects.filter(participants=request.user)
    
    # Count unread messages
    unread_counts = {}
    for conversation in conversations:
        unread_counts[conversation.id] = Message.objects.filter(
            conversation=conversation,
            is_read=False
        ).exclude(sender=request.user).count()
    
    context = {
        'conversations': conversations,
        'unread_counts': unread_counts,
    }
    
    return render(request, 'messages/inbox.html', context)

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, pk=conversation_id)
    
    # Check if the user is a participant
    if request.user not in conversation.participants.all():
        return HttpResponseForbidden("You are not authorized to view this conversation.")
    
    # Mark messages as read
    Message.objects.filter(
        conversation=conversation,
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            
            # Update conversation timestamp
            conversation.save()  # This will update the updated_at field
            
            return redirect('conversation_detail', conversation_id=conversation.id)
    else:
        form = MessageForm()
    
    messages_list = Message.objects.filter(conversation=conversation)
    
    context = {
        'conversation': conversation,
        'messages': messages_list,
        'form': form,
    }
    
    return render(request, 'messages/conversation_detail.html', context)

@login_required
def start_conversation(request, user_id=None, product_id=None):
    recipient = None
    product = None
    
    # If user_id is provided, get the recipient
    if user_id:
        recipient = get_object_or_404(User, pk=user_id)
        
        # Check if trying to message self
        if recipient == request.user:
            django_messages.error(request, "You cannot message yourself!")
            return redirect('inbox')
    
    # If product_id is provided, get the product and set recipient to seller
    if product_id:
        product = get_object_or_404(Product, pk=product_id)
        recipient = product.seller
        
        # Check if trying to message self
        if recipient == request.user:
            django_messages.error(request, "You cannot message yourself!")
            return redirect('product_detail', pk=product.pk)
    
    # Check if a conversation already exists
    existing_conversation = None
    if product:
        # Look for conversation about this product
        existing_conversation = Conversation.objects.filter(
            participants=request.user,
            product=product
        ).filter(participants=recipient).first()
    else:
        # Look for direct conversation with this user
        existing_conversation = Conversation.objects.filter(
            participants=request.user,
            product=None
        ).filter(participants=recipient).first()
    
    if existing_conversation:
        return redirect('conversation_detail', conversation_id=existing_conversation.id)
    
    if request.method == 'POST':
        form = ConversationForm(request.POST)
        if form.is_valid():
            # Create new conversation
            conversation = Conversation.objects.create(product=product)
            conversation.participants.add(request.user, recipient)
            
            # Create first message
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=form.cleaned_data['message']
            )
            
            django_messages.success(request, f"Message sent to {recipient.username}!")
            return redirect('conversation_detail', conversation_id=conversation.id)
    else:
        form = ConversationForm()
    
    context = {
        'form': form,
        'recipient': recipient,
        'product': product,
    }
    
    return render(request, 'messages/start_conversation.html', context)

@login_required
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, pk=conversation_id)
    
    # Check if the user is a participant
    if request.user not in conversation.participants.all():
        return HttpResponseForbidden("You are not authorized to delete this conversation.")
    
    if request.method == 'POST':
        conversation.delete()
        django_messages.success(request, "Conversation deleted!")
        return redirect('inbox')
    
    return render(request, 'messages/delete_conversation.html', {'conversation': conversation}) 