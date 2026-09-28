from django.db import models
from django.conf import settings

from SmartHire.jobs.models import Job
from SmartHire.resumes.models import Resume

# Create your models here.

class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        REVIEWING = 'REVIEWING', 'Reviewing'
        SHORTLISTED = 'SHORTLISTED', 'Shortlisted'
        REJECTED = 'REJECTED', 'Rejected'
        HIRED = 'HIRED', 'Hired'
        
        
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='application')
    application = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='application')
    resume = models.ForeignKey(Resume, settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_application')
    cover_letter = models.ForeignKey(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    applied_at = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('job', 'applicant')
