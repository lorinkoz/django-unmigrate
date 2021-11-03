django-unmigrate
================

.. image:: https://img.shields.io/badge/packaging-poetry-purple.svg
    :alt: Packaging: poetry
    :target: https://github.com/sdispater/poetry

.. image:: https://img.shields.io/badge/code%20style-black-black.svg
    :alt: Code style: black
    :target: https://github.com/ambv/black

.. image:: https://github.com/lorinkoz/django-unmigrate/workflows/code/badge.svg
    :alt: Build status
    :target: https://github.com/lorinkoz/django-unmigrate/actions

.. image:: https://coveralls.io/repos/github/lorinkoz/django-unmigrate/badge.svg?branch=master
    :alt: Code coverage
    :target: https://coveralls.io/github/lorinkoz/django-unmigrate?branch=master

.. image:: https://badge.fury.io/py/django-unmigrate.svg
    :alt: PyPi version
    :target: http://badge.fury.io/py/django-unmigrate

.. image:: https://pepy.tech/badge/django-unmigrate/month
    :alt: Downloads
    :target: https://pepy.tech/project/django-unmigrate/

|

If you are in a complex Django project, sometimes you will find yourself switching
between multiple branches, some of which can add a number of database migrations.
Before switching back to ``master`` you will have to unapply all migrations that
are specific to the current branch. In order to unapply these, you will have to
enter the migration that comes right before the first migration of the current
branch. If two or more apps are involved, you will have to do that for each one
of them.

If you leave your migration names unchanged, inferring the name of the right
migration to target is not too difficult, because they are prefixed by default
with a sequential number. Django also helps, being smart enough to let you use
an unambiguous prefix of any migration name. Add a merge migration and the
numbers will no longer be so obvious. Or if you have renamed your migration
files to drop the sequential numbers you will have to do the search manually.

With ``django-unmigrate`` you can speed up the process.

Usage
-----

Add ``django_unmigrate`` to your ``INSTALLED_APPS``. This is required to make
the ``unmigrate`` management command available.

Then, while standing on any branch, you will be able to use::

    python manage.py unmigrate master

Or if it's going to be ``master`` anyways, this will suffice::

    python manage.py unmigrate

And that's it!

A little deeper
---------------

Ok, you can do more than that.

Do you need to unapply your migrations from the same branch, a few commits
behind? Here's how::

    python manage.py unmigrate HEAD~12
    python manage.py unmigrate b13553d
    python manage.py unmigrate v1.33.7

Or if you only want to see the target migrations, do::

    python manage.py unmigrate --dry-run

Finally, if you just want to play with the app with no actual modifications in
the database, go ahead and unapply your migrations with ``fake``. Just don't
forget to apply them again at the end::

    python manage.py unmigrate --fake
    python manage.py migrate --fake

Contributing
------------

- Join the discussion at https://github.com/lorinkoz/django-unmigrate/discussions.
- PRs are welcome! If you have questions or comments, please use the link
  above.
- To run the test suite run ``make`` or ``make coverage``. The tests for this
  project live inside a small django project called ``dunm_sandbox``. Beware!
  This package uses Git to function, therefore, the tests expect a number of
  commit hashes inside this repository to be present and remain stable in order
  to function. See `this meta file`_ for further details.

.. _this meta file: https://github.com/lorinkoz/django-unmigrate/blob/master/dunm_sandbox/meta.py
