from django.urls import path
from . import views

urlpatterns = [
    path('find/',        views.find_skills,  name='find_skills'),
    path('add-skill/',   views.add_skill,    name='add_skill'),
    path('delete-skill/<int:skill_id>/',
         views.delete_skill, name='delete_skill'),
    path('connect/<int:user_id>/<str:skill_name>/',
         views.connect,      name='connect'),
]
