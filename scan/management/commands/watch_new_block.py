from time import sleep

from django.core.management import BaseCommand

from scan.helpers.last_block import get_last_height, set_cache_last_height


class Command(BaseCommand):
    help = "Watch new block"

    def handle(self, *args, **options):
        last_height = 0
        while True:
            height = get_last_height()
            if last_height != height:
                last_height = height
                print(f"New block: {height}")
                set_cache_last_height(height)
            sleep(1)
