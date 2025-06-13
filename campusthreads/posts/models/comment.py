from django.db import models
from campusthreads.base_model import BaseModel

class Comment(BaseModel):
    comment_content = models.CharField(max_length=255)

    author = models.ForeignKey(
        "accounts.User",
        related_name="comments",
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        "Post",
        related_name = "comments",
        on_delete=models.CASCADE
    )

    parent_comment = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        related_name="child_comments",
        on_delete=models.SET_NULL
    )

    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.id}"