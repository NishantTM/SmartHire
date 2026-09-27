from django.shortcuts import render, get_object_or_404, redirect
from.models import Job, Category, Application
from django.contrib import messages

# Create your views here.


def job_list(request):
    jobs = Job.objects.filter(is_active=True).select_related('category', 'employer')
    categories = Category.objects.all()
    
    query = request.GET.get('q')
    category_slug = request.GET.get('category')
    job_type = request.GET.get('type')
    
    if query:
        jobs = jobs.filter(title__icontains=query)
    if category_slug:
        jobs = jobs.filter(category__slug=category_slug)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
        
    context = {
        'jobs': jobs.order_by('-created_at'),
        'categories': categories,
    }
    return render(request, 'jobs/job_list.html', context)


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    
    # Check if logged-in user already applied
    has_applied = False
    if request.user.is_authenticated:
        has_applied = Application.objects.filter(job=job, applicant=request.user).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        if has_applied:
            messages.warning(request, "You have already applied for this position.")
            return redirect('job_detail', pk=job.pk)
        
        resume = request.FILES.get('resume')
        cover_letter = request.POST.get('cover_letter', '')
        
        if resume:
            Application.objects.create(
                job=job,
                applicant=request.user,
                resume=resume,
                cover_letter=cover_letter
            )
            messages.success(request, "Your application has been submitted successfully!")
            return redirect('job_detail', pk=job.pk)

    return render(request, 'jobs/job_detail.html', {'job': job, 'has_applied': has_applied})


def create_job(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        company_name = request.POST.get('company_name')
        location = request.POST.get('location')
        category_id = request.POST.get('category')
        job_type = request.POST.get('job_type')
        salary_range = request.POST.get('salary_range')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')

        # Basic manual validation
        if not title or not company_name or not category_id:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'jobs/job_form.html', {'categories': categories})

        category = get_object_or_404(Category, pk=category_id)

        # Create and save the Job instance
        job = Job.objects.create(
            title=title,
            company_name=company_name,
            location=location,
            category=category,
            job_type=job_type,
            salary_range=salary_range,
            description=description,
            requirements=requirements
        )

        messages.success(request, 'Job posted successfully!')
        return redirect('job_detail', pk=job.pk)

    return render(request, 'jobs/job_form.html', {'categories': categories})