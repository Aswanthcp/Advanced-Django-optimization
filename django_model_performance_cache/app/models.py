from django.db import models
from django.core.cache import cache


class PostQuerySet(models.QuerySet):
    def all(self):
        cache_key = "all_posts"
        cached_posts = cache.get(cache_key)

        if cached_posts is None:
            cached_posts = list(super().all())
            cache.set(cache_key, cached_posts)
        return cached_posts


class PostManager(models.Manager):  # Update inheritance
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    objects = PostManager()

    def save(self, *args, **kwargs):
        cache.delete("all_posts")  # Clear cache after saving
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cache.delete("all_posts")  # Clear cache after deletion
        super().delete(*args, **kwargs)
