from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, TransactionTestCase, override_settings

from dunm_sandbox.meta import COMMITS, PARENTS, MIGRATION_ZERO_COMMIT
from django_unmigrate.management.commands.unmigrate import Command as UnmigrateCommand


class UnmigrateCommandDryRunTestCase(TestCase):
    """
    Tests 'unmigrate' management command with --dry-run
    """

    def test_debug(self):
        unmigrate = UnmigrateCommand()
        unmigrate.from_argv = True  # Need to skip argv check
        call_command(unmigrate, dry_run=True)

    @override_settings(DEBUG=True)  # Django always uses DEBUG=False, need to skip the debug check
    def test_bad_ref(self):
        unmigrate = UnmigrateCommand()
        unmigrate.from_argv = True  # Need to skip argv check
        with self.assertRaises(CommandError) as ctx:
            call_command(unmigrate, "hopefully-unexisting-ref-in-my-own-git-repo")
        self.assertTrue(str(ctx.exception).startswith("Git says:"))

    @override_settings(DEBUG=True)  # Django always uses DEBUG=False, need to skip the debug check
    def test_migration_zero(self):
        unmigrate = UnmigrateCommand()
        unmigrate.from_argv = True  # Need to skip argv check
        with StringIO() as stdout:
            call_command(
                unmigrate, MIGRATION_ZERO_COMMIT, dry_run=True, no_color=True, stdout=stdout
            )  # It's required to strip colored output
            stdout.seek(0)
            self.assertEqual(stdout.read().strip(), "myapp zero")

    @override_settings(DEBUG=True)  # Django always uses DEBUG=False, need to skip the debug check
    def test_migration_parents(self):
        unmigrate = UnmigrateCommand()
        unmigrate.from_argv = True  # Need to skip argv check
        for commit, expected_migrations in COMMITS.items():
            expected_migrations.sort()  # We know tuple-sorting our migrations yields chronological order
            expected_parents = []
            if expected_migrations:
                expected_parents = PARENTS[expected_migrations[0]]
            with StringIO() as stdout:
                call_command(
                    unmigrate, commit, dry_run=True, no_color=True, stdout=stdout
                )  # It's required to strip colored output, skipping verbosity check on purpose
                stdout.seek(0)
                self.assertEqual(
                    set(stdout.read().strip().splitlines()), set(["{0} {1}".format(*x) for x in expected_parents])
                )


class UnmigrateCommandCleanTestCase(TransactionTestCase):
    """
    Tests 'unmigrate' management command with --clean
    """

    @patch("os.remove")
    @override_settings(DEBUG=True)  # Django always uses DEBUG=False, need to skip the debug check
    def test_full_unmigrate_by_commit(self, mocked_remove):
        unmigrate = UnmigrateCommand()
        unmigrate.from_argv = True  # Need to skip argv check
        for commit, expected_migrations in COMMITS.items():
            expected_migrations.sort()  # We know tuple-sorting our migrations yields chronological order
            expected_parents = []
            if expected_migrations:
                expected_parents = PARENTS[expected_migrations[0]]
            with StringIO() as stdout:
                call_command(unmigrate, commit, clean=True, stdout=stdout)
                stdout.seek(0)
                stdout_str = stdout.read()
                self.assertTrue(not expected_parents or "Unapplying " in stdout_str)
                self.assertTrue(not expected_parents or "Remove " in stdout_str)
                self.assertTrue(mocked_remove.called)
            with StringIO() as stdout:
                call_command("migrate", stdout=stdout)
                stdout.seek(0)
                self.assertTrue(not expected_parents or "Applying" in stdout.read())


class UnmigrateCommandTestCase(TransactionTestCase):  # In order to test migrations, must be TransactionTestCase
    """
    Tests 'unmigrate' management command
    """

    @override_settings(DEBUG=True)  # Django always uses DEBUG=False, need to skip the debug check
    def test_no_argv(self):
        with self.assertRaises(CommandError) as ctx:
            call_command("unmigrate")
        self.assertEqual(
            str(ctx.exception), "For your own protection, 'unmigrate' can only be run from the command line."
        )

    def test_debug(self):
        with self.assertRaises(CommandError) as ctx:
            call_command("unmigrate")
        self.assertEqual(str(ctx.exception), "Do not run with DEBUG=False, or pass --danger.")

    def test_debug_with_danger(self):
        unmigrate = UnmigrateCommand()
        unmigrate.from_argv = True  # Need to skip argv check
        call_command(unmigrate, danger=True)

    @override_settings(DEBUG=True)  # Django always uses DEBUG=False, need to skip the debug check
    def test_full_unmigrate_by_commit(self):
        unmigrate = UnmigrateCommand()
        unmigrate.from_argv = True  # Need to skip argv check
        for commit, expected_migrations in COMMITS.items():
            expected_migrations.sort()  # We know tuple-sorting our migrations yields chronological order
            expected_parents = []
            if expected_migrations:
                expected_parents = PARENTS[expected_migrations[0]]
            with StringIO() as stdout:
                call_command(unmigrate, commit, stdout=stdout)
                stdout.seek(0)
                self.assertTrue(not expected_parents or "Unapplying" in stdout.read())
            with StringIO() as stdout:
                call_command("migrate", stdout=stdout)
                stdout.seek(0)
                self.assertTrue(not expected_parents or "Applying" in stdout.read())

    @override_settings(DEBUG=True)  # Django always uses DEBUG=False, need to skip the debug check
    def test_full_unmigrate_zero(self):
        unmigrate = UnmigrateCommand()
        unmigrate.from_argv = True  # Need to skip argv check
        with StringIO() as stdout:
            call_command(unmigrate, MIGRATION_ZERO_COMMIT, stdout=stdout)
            stdout.seek(0)
            self.assertTrue("Unapplying" in stdout.read())
        with StringIO() as stdout:
            call_command("migrate", stdout=stdout)
            stdout.seek(0)
            self.assertTrue("Applying" in stdout.read())
