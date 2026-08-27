from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication URLs
    path('register/',  views.register_view,  name='register'),
    path('login/',     views.login_view,      name='login'),
    path('logout/',    views.logout_view,     name='logout'),
    path('dashboard/', views.dashboard_view,  name='dashboard'),

    # Skill Management URLs (NEW)
    path('add-skill/',              views.add_skill_view,    name='add_skill'),
    path('delete-skill/<int:skill_id>/',
         views.delete_skill_view, name='delete_skill'),
]
