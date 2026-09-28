from django.db import models
from django.conf import settings

# Create your models here.
class Companies(models.Model):
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='companies')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100)
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=25, blank=True, null=True)
    description = models.TextField(max_length=200)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
    