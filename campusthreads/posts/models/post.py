from django.db import models
from campusthreads.base_model import BaseModel

class Post(BaseModel):
    post_title = models.CharField(max_length=100)

    post_content = models.JSONField(default=dict)

    post_likes = models.PositiveIntegerField(default=0)

    author = models.ForeignKey(
        "accounts.User",
        related_name="posts",
        on_delete=models.SET_NULL,
        null=True
    )

    category = models.ForeignKey(
        "community.Category",
        related_name="posts",
        on_delete=models.SET_NULL,
        null=True
    )

    tag = models.CharField(max_length=10, default="")

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}"