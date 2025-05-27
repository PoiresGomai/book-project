from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.http import HttpResponse

def home_redirect(request):
    """Redirect root URL to manager app"""
    return redirect('/manager/')

def health_check(request):
    """Health check endpoint for Render.com"""
    return HttpResponse("OK", content_type="text/plain")

# Main URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin
    path('manager/', include('manager.urls')),  # Manager app
    path('health/', health_check, name='health_check'),  # Health check
    path('', home_redirect, name='home'),  # Root redirect
]
