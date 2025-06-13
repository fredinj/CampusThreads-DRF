from django.urls import path, include

from community.views import CategoryRequestViewSet


urlpatterns = [
    path('request/', CategoryRequestViewSet.as_view({
        'post': 'create',
        'get': 'list'
    }), name='category_requests'),

    path('request/pending/', CategoryRequestViewSet.as_view({'get': 'pending'}),
         name='pending-category-requests'),

    path('<int:pk>/approve/', CategoryRequestViewSet.as_view({'put': 'approve'}),
         name='approve-category-request'),

    path('<int:pk>/reject/', CategoryRequestViewSet.as_view({'put': 'reject'}),
         name='reject-category-request')
]