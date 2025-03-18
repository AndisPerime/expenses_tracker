"""
URL configuration for expenses_tracker project.
"""
from django.contrib import admin
from django.urls import path, include
from main_app import views as main_views

urlpatterns = [
    path('', include("main_app.urls")),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]
