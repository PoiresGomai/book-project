from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home_redirect(request):
    """Redirect root URL to public home page"""
    return redirect('/public/')

# Main URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin
    path('manager/', include('manager.urls')),  # Manager interface
    path('public/', include('manager.urls')),   # Public interface (for static compatibility)
    path('', home_redirect, name='home'),  # Root redirect
]
