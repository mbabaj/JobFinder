from celery import shared_task

@shared_task
def run_scraping():
    from scripts.scraper import run_scraper
    from scripts.scraper1 import run_scraper1
    from scripts.scraper2 import run_scraper2
    from scripts.remove_duplicates import run_rd
    run_scraper()
    run_scraper1()
    run_scraper2()
    run_rd()
    return "Scraping completed"