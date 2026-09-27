from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    
        class Role(models.TextChoices):
        
            JOB_SEEKER = "JOB_SEEKER", "job_seeker",
            RECRUITER = "RECRUITER", "recruiter",
            ADMIN = "ADMIN", "admin"
        
        role = models.CharField(max_length=20, choices=Role.choices,default=Role.JOB_SEEKER)

        email = models.EmailField(unique=True)
        
        phone = models.CharField(max_length=15)
        
        profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
        
        created_at = models.DateField(auto_now_add=True)
        
        updated_at = models.DateField(auto_now=True)
        
        def __str__(self):
            return f"{self.username} - {self.get_role_display()}"
        
        