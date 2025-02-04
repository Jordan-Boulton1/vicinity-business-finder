from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'businesses', views.BusinessViewSet)

app_name = 'businesses'

urlpatterns = [
    path('', include(router.urls)),
]