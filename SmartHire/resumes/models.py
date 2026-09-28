from django.db import models
from django.conf import settings

# Create your models here.
class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=300)
    file = models.ImageField(upload_to='resume/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
