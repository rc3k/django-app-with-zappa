from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from acme.current_account import views

router = routers.DefaultRouter()
router.register(r'application', views.ApplicationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
