from django.core.management import BaseCommand

from scan.tasks import aggregate_multiouts


class Command(BaseCommand):
    help = "Aggregate MultiOut transactions"

    def handle(self, *args, **options):
        aggregate_multiouts()
