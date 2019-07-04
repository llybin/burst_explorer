from django.core.management import BaseCommand

from scan.peers import peer_cmd


class Command(BaseCommand):
    help = "Peers scanning"

    def handle(self, *args, **options):
        peer_cmd()
