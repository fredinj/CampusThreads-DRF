from django.db import models
from campusthreads.base_model import BaseModel

class Reaction(BaseModel):
    TYPE_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike')
    ]

    user = models.ForeignKey(
        "accounts.User", 
        related_name="reactions",
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        "Post",
        related_name="reactions",
        on_delete=models.CASCADE
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.email} {self.reaction_type}d {self.post}"
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'post']),  # Query optimization
        ]
        unique_together = ['user', 'post']

    def __str__(self):
        return f"{self.id}"