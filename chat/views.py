from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Message
from skills.models import Connection

User = get_user_model()


@login_required
def inbox(request):
    """Show all conversations the logged-in user is part of."""
    me = request.user

    # Get all connections involving this user
    connections = Connection.objects.filter(
        requester=me
    ) | Connection.objects.filter(
        provider=me
    )
    connections = connections.select_related(
        'requester', 'provider').distinct()

    # Build conversation list
    conversations = []
    seen = set()
    for conn in connections:
        other = conn.provider if conn.requester == me else conn.requester
        skill = conn.skill_name
        key = f"{min(me.id, other.id)}_{max(me.id, other.id)}_{skill}"
        if key in seen:
            continue
        seen.add(key)

        # Get last message
        last_msg = Message.objects.filter(
            sender=me, receiver=other, skill_name=skill
        ) | Message.objects.filter(
            sender=other, receiver=me, skill_name=skill
        )
        last_msg = last_msg.order_by('-timestamp').first()

        # Count unread messages
        unread = Message.objects.filter(
            sender=other, receiver=me,
            skill_name=skill,
            deleted_by_receiver=False,
        ).exclude(sender=me).count()

        conversations.append({
            'other':    other,
            'skill':    skill,
            'last_msg': last_msg,
            'unread':   unread,
        })

    return render(request, 'chat/inbox.html', {'conversations': conversations})


@login_required
def chat_room(request, user_id, skill_name):
    """Open a chat window between me and another user about a skill."""
    me = request.user
    other = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                sender=me,
                receiver=other,
                skill_name=skill_name,
                content=content,
            )
        return redirect('chat_room', user_id=user_id, skill_name=skill_name)

    # Load all visible messages between these two users for this skill
    all_messages = Message.objects.filter(
        sender=me, receiver=other, skill_name=skill_name
    ) | Message.objects.filter(
        sender=other, receiver=me, skill_name=skill_name
    )
    all_messages = all_messages.order_by('timestamp')
    visible = [m for m in all_messages if m.is_visible_to(me)]

    # Get other conversations for the sidebar
    connections = Connection.objects.filter(
        requester=me
    ) | Connection.objects.filter(
        provider=me
    )
    conversations = []
    seen = set()
    for conn in connections.select_related('requester', 'provider'):
        o = conn.provider if conn.requester == me else conn.requester
        sk = conn.skill_name
        key = f"{min(me.id, o.id)}_{max(me.id, o.id)}_{sk}"
        if key in seen:
            continue
        seen.add(key)
        conversations.append({'other': o, 'skill': sk})

    return render(request, 'chat/chat_room.html', {
        'other':         other,
        'skill_name':    skill_name,
        'messages':      visible,
        'conversations': conversations,
    })


@login_required
def delete_message(request, message_id):
    """Soft-delete a message for the requesting user."""
    msg = get_object_or_404(Message, id=message_id)
    me = request.user

    if me == msg.sender:
        msg.deleted_by_sender = True
    elif me == msg.receiver:
        msg.deleted_by_receiver = True
    msg.save()

    return redirect('chat_room',
                    user_id=msg.receiver.id if me == msg.sender else msg.sender.id,
                    skill_name=msg.skill_name)
