import requests
from bs4 import BeautifulSoup
import random
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "polyjobs.settings")
django.setup()

from scraper.models import Job
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"
]

def run():
    url = "https://jobs.telegrafi.com/"
    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    job_data = []

    for job_item in soup.select("div.job-info"):
        a_tag = job_item.find("a", href=True)
        if not a_tag:
            continue

        link = a_tag["href"]

        img_tag = a_tag.find("img", src=True)
        image_url = img_tag["src"] if img_tag else ""

        job_name_div = a_tag.find("div", class_="job-name")
        title = job_name_div.find("h3").get_text(strip=True) if job_name_div and job_name_div.find("h3") else ""

        city = job_name_div.find("span", class_="puna-location").get_text(strip=True) if job_name_div and job_name_div.find("span", class_="puna-location") else ""

        job_schedule_div = a_tag.find("div", class_="job-schedule")
        expiration = job_schedule_div.get_text(strip=True) if job_schedule_div else ""
    
        if link:  # make sure link exists
            # Check if job already exists
            job, created = Job.objects.update_or_create(
                link=link,
                defaults={
                    "image_url": image_url,
                    "title": title,
                    "city": city,
                    "expiration": expiration
                }
            )