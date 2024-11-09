from django.urls import path, include
from django.contrib import admin
from lists import views as list_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', list_views.home_page, name='home'),
    path('lists/', include('lists.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]
