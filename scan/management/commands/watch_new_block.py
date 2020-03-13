from time import sleep

from django.core.management import BaseCommand

from scan.caching_data.last_height import CachingLastHeight


class Command(BaseCommand):
    help = "Watch new block"

    def handle(self, *args, **options):
        last_height = 0
        while True:
            height = CachingLastHeight().live_data
            if last_height != height:
                last_height = height
                print(f"New block: {height}")
                CachingLastHeight().update_data(height)
            sleep(1)
