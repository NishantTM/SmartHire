from django.db import models
from django.contrib.auth import get_user_model

# Fetch the active user model
User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# IMPORTANT: Ensure 'class Job' has NO spaces/tabs in front of it!
class Job(models.Model):
    # Outer parentheses wrap ALL inner choice tuples separated by commas
    JOB_TYPE_CHOICES = (
        ("FT", "Full-Time"),
        ("PT", "Part-Time"),
        ("CT", "Contract"),
        ("IT", "Internship"),
        ("RM", "Remote"),
    )

    employer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="jobs"
    )
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="jobs"
    )
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=200)
    job_type = models.CharField(
        max_length=200, choices=JOB_TYPE_CHOICES, default="FT"
    )
    salary_range = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company_name}"


class Application(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("reviewed", "Reviewed"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="applications"
    )
    resume = models.FileField(upload_to="resumes/")
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "applicant")

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"