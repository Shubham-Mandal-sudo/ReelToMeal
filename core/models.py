from django.db import models
from django.contrib.auth.models import User

class RecipeHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    video_url = models.URLField()
    # FIX: Added recipe_name field
    recipe_name = models.CharField(max_length=255, default="Unknown Recipe") 
    recipe_data = models.JSONField() 
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.recipe_name}"