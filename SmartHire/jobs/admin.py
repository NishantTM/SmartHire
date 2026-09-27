from django.contrib import admin

# Register your models here.
from . models import Category, Job, Application

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'category', 'job_type', 'is_active', 'created_at')
    list_filter = ('job_type', 'is_active', 'category')
    search_fields = ('title', 'company_name', 'location')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'job', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')