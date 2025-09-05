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

def run_scraper1():
    url = "https://ofertapune.net/"
    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    for jobcnt in soup.select("div.jobListCnts"):
        img_div = jobcnt.select_one("div.jobListImage")
        image_url = img_div["data-background-image"] if img_div and img_div.has_attr("data-background-image") else None

        link_tag = jobcnt.select_one("a")
        link = link_tag["href"] if link_tag and link_tag.has_attr("href") else None

        inner = jobcnt.select_one("div.jobListCntsInner")
        title = city = expiration = None
        if inner:
            title_tag = inner.select_one("div.jobListTitle")
            city_tag = inner.select_one("div.jobListCity")
            exp_tag = inner.select_one("div.jobListExpires")

            title = title_tag.get_text(strip=True) if title_tag else None
            city = city_tag.get_text(strip=True) if city_tag else None
            expiration = exp_tag.get_text(strip=True) if exp_tag else None

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