from django.db import models
from django.contrib.auth.models import User

class RecipeHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    video_url = models.URLField()
    recipe_data = models.JSONField() # Stores the parsed Gemini JSON response
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.video_url}"