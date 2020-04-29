from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS

from django_unmigrate.core import get_targets, GitError


class Command(BaseCommand):
    help = "Unapplies migrations that were added in relation to the passed Git ref."

    def add_arguments(self, parser):
        parser.add_argument(
            "ref", nargs="?", default="master", help="Git ref to compare existing migrations.",
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
            "--dry-run", action="store_true", help="Just print the target migrations.",
        )
        parser.add_argument(
            "--kamikazee", action="store_true", help="Ignore DEBUG=True and run the command anyways.",
        )

    def run_from_argv(self, argv):
        self.from_argv = True
        super().run_from_argv(argv)

    def handle(self, *args, **options):
        if not settings.DEBUG and not options["kamikazee"]:
            raise CommandError("Do not run with DEBUG=True, or pass --kamikazee.")
        if not getattr(self, "from_argv", False):
            raise CommandError("For your own protection, 'unmigrate' can only be run from the command line.")
        try:
            targets = get_targets(options["database"], options["ref"]).items()
        except GitError as error:
            raise CommandError("Git says: {}".format(error))
        for key, targets in targets:
            for app, migration in targets:
                if options["dry_run"] and options["verbosity"] >= 1:
                    self.stdout.write(self.style.MIGRATE_LABEL("{}.{}".format(app, migration)))
                else:
                    management.call_command(
                        "migrate", app, migration, fake=options["fake"], verbosity=options["verbosity"]
                    )