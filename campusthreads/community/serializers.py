from rest_framework import serializers

from community.models import CategoryRequest, Category

class CategoryRequestSerializer(serializers.ModelSerializer):
    categoryName = serializers.CharField(source='category_name')
    _id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = CategoryRequest
        fields = ('_id', 'categoryName', 'description', 'requested_by', 'status', 'tags', 'is_active')
        read_only_fields = ('_id', 'requested_by', 'status', 'is_active')


class CategorySerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Category
        fields = ('_id', 'name', 'description', 'tags')
        read_only_fields = ('_id', 'name')
