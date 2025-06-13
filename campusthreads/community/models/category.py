from django.db import models
from campusthreads.base_model import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=20, unique=True)
    
    description = models.CharField(max_length=255)
    
    requested_by = models.ForeignKey(
        "accounts.User",
        related_name="categories_created",
        on_delete=models.SET_NULL,
        null=True
    )
    
    category_request = models.ForeignKey(
        "CategoryRequest",
        related_name="category",
        on_delete=models.SET_NULL,
        null=True
    )

    tags = models.JSONField(default=list)  

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"