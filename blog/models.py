from django.db import models
from django_cleanup import cleanup


# Create your models here.

@cleanup.select
class Blog(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to="blog/")

    def __str__(self):
        return f"{self.title} - {self.description[:35]}"

    class Meta:
        ordering = ['-id']
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    @property
    def List_Blog(self):
        return Blog.objects.filter()
