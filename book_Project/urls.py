from django.contrib import admin
from django.urls import path, include

# Main URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin
    path('manager/', include('manager.urls')),  # Public interface at /manager/
    path('', include('manager.urls')),  # Also accessible from root
]
