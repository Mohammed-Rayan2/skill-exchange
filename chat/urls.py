from django.urls import path
from . import views

urlpatterns = [
    path('chat/',
         views.inbox,          name='inbox'),
    path('chat/<int:user_id>/<str:skill_name>/',
         views.chat_room,      name='chat_room'),
    path('chat/delete/<int:message_id>/',
         views.delete_message, name='delete_message'),
]
