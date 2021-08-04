from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length= 30)
    img = models.ImageField()
    timestamp = models.DateTimeField(auto_now_add= True)
    content = models.TextField()

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'post'
        verbose_name_plural = 'posts'
    
    def __str__(self):
        return self.title