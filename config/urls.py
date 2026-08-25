from django.contrib import admin
from django.urls import path, include
from skills.views import home_view

urlpatterns = [
    # Home page — directly mapped here
    path('', home_view, name='home_page'),

    # Admin
    path('admin/', admin.site.urls),

    # Google OAuth
    path('accounts/', include('allauth.urls')),

    # Our app URLs
    path('', include('accounts.urls')),
    path('', include('skills.urls')),
    path('', include('chat.urls')),
]
