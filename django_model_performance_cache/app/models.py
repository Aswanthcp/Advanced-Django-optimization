from django.db import models
from django.core.cache import cache


class PostQuerySet(models.QuerySet):
    def all(self):
        cache_key = "all_posts"
        cached_posts = cache.get(cache_key)

        if cached_posts is None:
            cached_posts = list(super().all())
            cache.set(cache_key, cached_posts, timeout=3600)
        return cached_posts


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    objects = PostManager()

    def save(self, *args, **kwargs):
        cache.delete("all_posts")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cache.delete("all_posts")
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

    @classmethod
    def get_cache_key(cls):
        return f"all_posts_{cls._meta.app_label}_{cls._meta.model_name}"
