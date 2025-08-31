from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from .models import Favorite, Job
from django.db.models import Q
from django.core.paginator import Paginator
def job_list(request):
    job_queryset = Job.objects.all().order_by('-id')  # adjust ordering as you like
    paginator = Paginator(job_queryset, 80)  # 80 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query = request.GET.get("q")
    city = request.GET.get("city")

    jobs = Job.objects.all()

    # Apply search filter
    if query:
        words = query.split()
        for word in words:
            jobs = jobs.filter(
                Q(title__icontains=word)
            )
        paginator = Paginator(jobs, 80)  # 80 jobs per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    # Apply city filter
    if city:
        jobs = jobs.filter(city=city)
        paginator = Paginator(jobs, 80)  # 80 jobs per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


    # Get unique cities for dropdown
    cities = Job.objects.values_list("city", flat=True).distinct()

    return render(request, "job_list.html", {
        "jobs": jobs,
        "cities": cities,
        "page_obj": page_obj,
    })
@login_required
def my_favorites(request):
    jobs = request.user.favorite_jobs.all()
    return render(request, 'my_favorites.html', {'jobs': jobs})

@login_required
@require_POST
def favorite_toggle(request, pk):
    job = get_object_or_404(Job, id=pk)

    if job in request.user.favorite_jobs.all():
        request.user.favorite_jobs.remove(job)
        is_favorited = False
    else:
        request.user.favorite_jobs.add(job)
        is_favorited = True

    # If it's an AJAX request, return JSON
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"is_favorited": is_favorited})

    # Fallback for non-AJAX requests
    return redirect(request.META.get('HTTP_REFERER', 'jobs_list'))