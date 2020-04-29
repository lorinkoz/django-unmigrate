from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS

from django_unmigrate.core import get_targets


class Command(BaseCommand):
    help = "Unapplies migrations that were added in the current branch, relative to the passed branch."

    def add_arguments(self, parser):
        parser.add_argument(
            "branch", nargs="?", default="master", help="Branch to compare existing migrations with.",
        )
        parser.add_argument(
            "--database",
            default=DEFAULT_DB_ALIAS,
            help='Nominates a database to synchronize. Defaults to the "default" database.',
        )
        parser.add_argument(
            "--fake", action="store_true", help="Mark migrations as run without actually running them.",
        )
        parser.add_argument(
            "--kamikazee", action="store_true", help="Ignore DEBUG=True and run the command anyways.",
        )

    def handle(self, *args, **options):
        if not settings.DEBUG and not options["kamikazee"]:
            raise CommandError("Do not run with DEBUG=True, or pass --kamikazee.")
        for key, targets in get_targets(options["database"], options["branch"]).items():
            for app, migration in targets:
                management.call_command("migrate", app, migration, fake=options["fake"], verbosity=options["verbosity"])
