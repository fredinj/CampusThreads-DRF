from rest_framework import serializers
from django.shortcuts import get_object_or_404

from posts.models import Post, Comment
from community.models import Category


class UserPostSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Post
        fields = ('_id', 'post_title')
        read_only_fields = ('_id', 'post_title')


class UserCommentSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model=Comment
        fields = ('_id', 'comment_content')


class PostSerializer(serializers.Serializer):
    post_title = serializers.CharField(max_length=100)
    post_content = serializers.JSONField(default=dict)
    tag = serializers.CharField(max_length=10, default="")
    category_id = serializers.IntegerField()

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['author'] = request.user
        
        category = get_object_or_404(Category, id=validated_data.pop('category_id'))
        validated_data['category'] = category

        return Post.objects.create(**validated_data)
    
    def to_representation(self, instance):
        return {
            'post_title': instance.post_title,
            'post_content': instance.post_content,
            'post_likes': instance.post_likes,
            'author': instance.author.first_name if instance.author else None,
            'author_id': instance.author.id,
            'category_id': instance.category.id,
            'tag': instance.tag,
            'is_deleted': instance.is_deleted,
            'category_name': instance.category.name,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }

class CommentsFetchSerializer(serializers.ModelSerializer):

    _id = serializers.IntegerField(source="id", read_only=True)
    commentContent = serializers.CharField(source="comment_content")
    parentComment = serializers.PrimaryKeyRelatedField(
        queryset = Comment.objects.all(),
        allow_null=True,
        required=False,
        source="parent_comment"
    )

    class Meta:
        model = Comment
        fields = ("_id", "author", "post", "commentContent", "parentComment")
        read_only_fields = ("_id", "author", "post", "parentComment")


class PostsFetchSerializer(serializers.ModelSerializer):

    _id = serializers.IntegerField(source='id', read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    author = serializers.CharField(source='author.first_name', read_only=True)

    class Meta:
        model = Post
        fields = ('_id', 'author_id', 'author', 'post_title', 'post_content', 'post_likes', 'category', 'tag')
        read_only_fields = ('post_title', 'author', 'category', 'tag')