from django.urls import path, include

from posts.views import CreatePostApiView


urlpatterns = [
    path('', CreatePostApiView.as_view(), name='create-post-endpoint')
]