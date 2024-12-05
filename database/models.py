from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Rating(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="ratings", on_delete=models.CASCADE)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'post')

        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['user'])
        ]

