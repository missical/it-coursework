from .models import Message, Conversation

def unread_message_count(request):
    """
    Context processor to count unread messages for the current user.
    """
    count = 0
    if request.user.is_authenticated:
        # Get all conversations where the user is a participant
        conversations = Conversation.objects.filter(participants=request.user)
        
        # Count unread messages in those conversations
        for conversation in conversations:
            count += Message.objects.filter(
                conversation=conversation,
                is_read=False
            ).exclude(sender=request.user).count()
    
    return {'unread_message_count': count} 