from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from community.models import Category, CategoryRequest
from community.serializers import CategoryRequestSerializer, CategorySerializer
from campusthreads.permissions import IsAdmin, IsTeacherOrAdmin

class CategoryRequestViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    '''
    This viewset creates and lists category requests using the Mixins
    and update the requests using the custom action methods
    '''
    http_method_names = ['get', 'post', 'put']
    queryset = CategoryRequest.objects.all()
    serializer_class = CategoryRequestSerializer

    # set requested by on category request creation
    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user)

    # /request/pending
    @action(detail=False, methods=['get'])
    def pending(self, request):
        pending_requests = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(pending_requests, many=True)
        return Response(serializer.data)
    
    # /:id/approve
    @action(detail=True, methods=['put'])
    def approve(self, request, pk=None):
        instance = self.get_object()
        if instance.status == 'approved':
            return Response(
                {'error': 'Request already approved'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                category = Category.objects.create(
                    name=instance.category_name,
                    description=instance.description,
                    requested_by=instance.requested_by,
                    category_request = instance,
                    tags=instance.tags
                )
                
                instance.status = 'approved'
                instance.save()
        except Exception as e:
            return Response(
                {"error": f"Failed to create a category {str(e)}"},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(self.get_serializer(instance).data)
    
    # /:id/reject
    @action(detail=True, methods=['put'])
    def reject(self, request, pk=None):
        instance = self.get_object()
        instance.status = 'rejected'
        instance.save()
        return Response(self.get_serializer(instance).data)
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsTeacherOrAdmin()]
        elif self.action in ['list', 'pending', 'approve', 'reject']:
            return [IsAdmin()]
        return []
        

class CategoryViewSet(ListModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    http_method_names = ['get', 'put', 'delete']
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # custom url path and url name for DRF router
    @action(detail=True, methods=['put'], url_path='update', url_name='update-category')
    def update_category(self, request, pk=None):
        instance = self.get_object()        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
    def get_permissions(self):
        if self.action in ['update_category', 'destroy']:
            return [IsTeacherOrAdmin()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return []