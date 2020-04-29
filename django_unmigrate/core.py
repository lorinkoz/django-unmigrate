import os
import sys

from django.conf import settings
from django.db import connections
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.executor import MigrationExecutor

from git import Repo

# TODO: improve migration detection
# settings.MIGRATION_MODULES = {app_string: module_location_string}


def get_targets(database, branch="master"):
    # Getting repo
    pathname = os.path.dirname(sys.argv[0])
    repo = Repo(os.path.abspath(pathname), search_parent_directories=True)
    # Getting diff
    here = set(repo.git.ls_tree("--name-only", "-r", "HEAD").splitlines())
    there = set(repo.git.ls_tree("--name-only", "-r", branch).splitlines())
    migration_files = [x for x in here - there if "migrations/" in x]
    # Constructing migration targets
    targets = [(f.split(os.sep)[-3], f.split(os.sep)[-1].split(".")[0]) for f in migration_files]
    # Preparing executor
    connection = connections[database]
    connection.prepare_database()
    loader = MigrationLoader(connection)
    executor = MigrationExecutor(connection)
    # Final move
    plan_dict = {target: set(loader.graph.backwards_plan(target)) for target in targets}
    final_targets = []
    for target, plan in plan_dict.items():
        if any([plan & i_plan == plan for i_plan in plan_dict.values() if i_plan != plan]):
            continue
        final_targets.append(target)
    return {target: [x.key for x in loader.graph.node_map[target].parents] for target in final_targets}
