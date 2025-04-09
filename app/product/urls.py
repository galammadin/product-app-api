"""
URL mappings for the product app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from product import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('tags', views.TagViewSet)
router.register('categories', views.CategoryViewSet)

app_name = 'product'

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
    path('frontend/', views.ProductFrontendView.as_view(), name='frontend'),
    path('test/', views.TestView.as_view(), name='test'),
]
