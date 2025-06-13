from django.urls import path, include
from rest_framework import routers

from community.views import CategoryRequestViewSet, CategoryViewSet

router = routers.DefaultRouter()

router.register(r'', CategoryViewSet)

urlpatterns = [
    # category request endpoints
    path('request/', CategoryRequestViewSet.as_view({
        'post': 'create',
        'get': 'list'
    }), name='category_requests'),

    path('request/pending/', CategoryRequestViewSet.as_view({'get': 'pending'}),
         name='pending-category-requests'),

    path('<int:pk>/approve/', CategoryRequestViewSet.as_view({'put': 'approve'}),
         name='approve-category-request'),

    path('<int:pk>/reject/', CategoryRequestViewSet.as_view({'put': 'reject'}),
         name='reject-category-request'),

    # category endpoints
    path('', include(router.urls))
]