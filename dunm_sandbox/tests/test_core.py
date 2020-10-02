from django.test import TestCase

from dunm_sandbox.meta import COMMITS, PARENTS
from django_unmigrate.core import GitError, get_added_migrations, get_parents_from_targets, get_targets


class GetAddedMigrationsTestCase(TestCase):
    """
    Tests core.get_added_migrations
    """

    def test_by_commit(self):
        for commit, expected_migrations in COMMITS.items():
            response = get_added_migrations(commit)
            self.assertEqual(set(response), set(expected_migrations))

    def test_by_commit_with_error(self):
        with self.assertRaises(GitError):
            get_added_migrations("hopefully-non-existing-ref")


class GetParentsFromTargetsTestCase(TestCase):
    """
    Tests core.get_parents_from_targets
    """

    def test_by_migration(self):
        for child, expected_parents in PARENTS.items():
            parents = get_parents_from_targets([child])
            self.assertEqual(set(parents), set(expected_parents))

    def test_overlapping_targets(self):
        parents = get_parents_from_targets(
            [("myapp", "0005_auto_20200502_0149"), ("myapp", "0004_merge_20200502_0148")]
        )
        self.assertEqual(set(parents), set([("myapp", "0003_mymodel_is_active")]))


class GetTargetsTestCase(TestCase):
    """
    Tests core.get_targets
    """

    def test_by_commit(self):
        for commit, expected_migrations in COMMITS.items():
            expected_migrations.sort()  # We know tuple-sorting our migrations yields chronological order
            expected_parents = []
            if expected_migrations:
                expected_parents = PARENTS[expected_migrations[0]]
            (added_targets, parent_target) = get_targets(ref=commit)
            self.assertEqual(set(added_targets), set(expected_migrations))
            self.assertEqual(set(parent_target), set(expected_parents))
