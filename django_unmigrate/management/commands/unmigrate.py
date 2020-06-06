from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS

from django_unmigrate.core import get_targets, GitError
from django_unmigrate.settings import MAIN_BRANCH

import os


class Command(BaseCommand):
    help = "Unapplies migrations that were added in relation to the passed Git ref."

    def add_arguments(self, parser):
        parser.add_argument(
            "ref", nargs="?", default=MAIN_BRANCH, help="Git ref to compare existing migrations.",
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
            "--danger", action="store_true", help="Ignore DEBUG=False and run the command anyways.",
        )
        parser.add_argument(
            "--clean", action="store_true", help="Delete migration files after they get unmigrated.",
        )

    def run_from_argv(self, argv):  # pragma: no cover
        self.from_argv = True
        super().run_from_argv(argv)

    def handle(self, *args, **options):
        if not settings.DEBUG and not options["danger"] and not options["dry_run"]:
            raise CommandError("Do not run with DEBUG=False, or pass --danger.")

        if not getattr(self, "from_argv", False):
            raise CommandError("For your own protection, 'unmigrate' can only be run from the command line.")

        try:
            (added_targets, parent_targets) = get_targets(options["database"], options["ref"])
        except GitError as error:
            raise CommandError("Git says: {}".format(error))

        command = "python manage.py migrate" if options["verbosity"] > 1 else ""

        for app, migration in parent_targets:
            if migration is None:
                migration = "zero"

            if options["dry_run"] and options["verbosity"] >= 1:
                self.stdout.write(
                    self.style.MIGRATE_HEADING(
                        "{command} {app} {migration}".format(command=command, app=app, migration=migration)
                    )
                )
            else:
                management.call_command(
                    "migrate",
                    app,
                    migration,
                    fake=options["fake"],
                    no_color=options["no_color"],
                    verbosity=options["verbosity"],
                    stdout=self.stdout,
                    stderr=self.stderr,
                )

        if options["clean"]:
            for (app, migration) in added_targets:
                file_name = f"{app}/migrations/{migration}.py"
                self.stdout.write(self.style.MIGRATE_HEADING(f"Remove {file_name}"))
                os.remove(file_name)
