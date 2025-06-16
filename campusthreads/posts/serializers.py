from rest_framework.serializers import ModelSerializer, CharField, JSONField, IntegerField, PrimaryKeyRelatedField

from posts.models import Post, Comment


class UserPostSerializer(ModelSerializer):
    _id = IntegerField(source='id', read_only=True)

    class Meta:
        model = Post
        fields = ('_id', 'post_title')
        read_only_fields = ('_id', 'post_title')


class UserCommentSerializer(ModelSerializer):
    _id = IntegerField(source='id', read_only=True)

    class Meta:
        model=Comment
        fields = ('_id', 'comment_content')


class CommentSerializer(ModelSerializer):

    _id = IntegerField(source="id", read_only=True)
    commentContent = CharField(source="comment_content")
    parentComment = PrimaryKeyRelatedField(
        queryset = Comment.objects.all(),
        allow_null=True,
        required=False,
        source="parent_comment"
    )

    class Meta:
        model = Comment
        fields = ("_id", "author", "post", "commentContent", "parentComment")
        read_only_fields = ("_id", "author", "post", "parentComment")


class PostSerializer(ModelSerializer):

    _id = IntegerField(source='id', read_only=True)
    author_id = IntegerField(source='author.id', read_only=True)
    author = CharField(source='author.first_name', read_only=True)

    class Meta:
        model = Post
        fields = ('_id', 'author_id', 'author', 'post_title', 'post_content', 'post_likes', 'category', 'tag')
        read_only_fields = ('post_title', 'author', 'category', 'tag')