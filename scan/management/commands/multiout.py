from django.core.management import BaseCommand

from scan.multiout import aggregate_cmd, clean_out_all_cmd, delete_greater_height_cmd


class Command(BaseCommand):
    help = "MultiOut transactions aggregation"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clean-out-all", action="store_true", help="Truncate MultiOut table"
        )

        parser.add_argument(
            "--delete-greater-height",
            type=int,
            help="Delete data greater height",
            default=None,
        )

    def handle(self, *args, **options):
        if options["clean_out_all"]:
            clean_out_all_cmd()
            print("All aggregated data was cleaned out")

        elif options["delete_greater_height"]:
            delete_greater_height_cmd(options["delete_greater_height"])
            print(
                f'Aggregated data was deleted with height greater {options["delete_greater_height"]}'
            )

        else:
            aggregate_cmd()
