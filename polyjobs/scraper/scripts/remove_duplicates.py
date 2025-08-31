import os
import django
from collections import defaultdict

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "polyjobs.settings")
django.setup()

from scraper.models import Job

def run():
    seen = set()
    duplicates = []

    for job in Job.objects.all():
        identifier = (job.title.strip(), job.city.strip(), job.expiration.strip())

        if identifier in seen:
            duplicates.append(job.id)
        else:
            seen.add(identifier)

    if duplicates:
        Job.objects.filter(id__in=duplicates).delete()