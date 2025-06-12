from django.db import models
from campusthreads.base_model import BaseModel

class CategoryRequest(BaseModel):
    STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]

    category_name = models.CharField(max_length=20)
    
    description = models.CharField(max_length=255)
    
    requested_by = models.ForeignKey(
        "accounts.User",
        related_name="category_requests",
        on_delete=models.SET_NULL,
        null=True
    )

    status = models.CharField(max_length=10, choices=STATUS, default='pending')

    tags = models.JSONField(default=list)