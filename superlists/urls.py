from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lists.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]
