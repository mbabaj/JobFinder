from django.db import models
from django.conf import settings
# Create your models here
class Job(models.Model):
    link = models.URLField(max_length=500)
    image_url = models.URLField(max_length=500)
    title = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    expiration = models.CharField(max_length=100)
    favorited_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Favorite',
        related_name='favorite_jobs',
        blank=True,
    )
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'job'], name='unique_user_job_favorite')
        ]
        indexes = [models.Index(fields=['user', 'job'])]