from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/',include('users.urls')),
    path('api/utilities/',include('utilities.urls')),
    path('api/packages/',include('packages.urls')),
    path('api/home/',include('home.urls')),
    path('api/booking/',include('booking.urls')),
    path('api/experience/',include('experience.urls')),
    path('', include('admin_material.urls')),
    
    
]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
