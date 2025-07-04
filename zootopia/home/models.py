from django.db import models


# Create your models here.
class Items(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    descripion = models.TextField(null=True, blank=True)
    imgurl = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title