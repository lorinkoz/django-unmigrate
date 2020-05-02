django-unmigrate
================

.. image:: https://img.shields.io/badge/packaging-poetry-purple.svg
    :alt: Packaging: poetry
    :target: https://github.com/sdispater/poetry

.. image:: https://img.shields.io/badge/code%20style-black-black.svg
    :alt: Code style: black
    :target: https://github.com/ambv/black

.. image:: https://badges.gitter.im/Join%20Chat.svg
    :alt: Join the chat at https://gitter.im/django-unmigrate
    :target: https://gitter.im/django-unmigrate/community?utm_source=share-link&utm_medium=link&utm_campaign=share-link

.. image:: https://github.com/lorinkoz/django-unmigrate/workflows/code/badge.svg
    :alt: Build status
    :target: https://github.com/lorinkoz/django-unmigrate/actions

.. image:: https://coveralls.io/repos/github/lorinkoz/django-unmigrate/badge.svg?branch=master
    :alt: Code coverage
    :target: https://coveralls.io/github/lorinkoz/django-unmigrate?branch=master

.. image:: https://badge.fury.io/py/django-unmigrate.svg
    :alt: PyPi version
    :target: http://badge.fury.io/py/django-unmigrate

.. image:: https://img.shields.io/pypi/dm/django-unmigrate
    :alt: Downloads

|

If you are in a complex Django project, sometimes you will find yourself switching
between multiple branches, some of which can add a number of database migrations.
Before switching back to ``master`` you will have to unapply all migrations that
are specific to the current branch. To make things worse, in order to unapply
Django migrations, you have to enter the migration that comes right before the
first migration of the current branch. It's not that big of a deal, Django is
smart enough to let you use an unambiguos prefix of any migration, but with
this package you can speed things up a little bit.

While standing on any branch, you can use::

    python manage.py unmigrate master

Or if it's going to be ``master`` anyways, this will suffice::

    python manage.py unmigrate

And that's it!

A little deeper
---------------

Ok, you can do more than that.

Do you need to unapply your migrations from the same branch, a few commits
behind? Here's how::

    python manage.py unmigrate HEAD~5
    python manage.py unmigrate af332b
    python manage.py unmigrate v1.33.7

If you only want to see the target migrations::

    python manage.py unmigrate --dry-run

And if you just want to play with this, go ahead and unapply your migrations
with ``fake``. Just don't forget to apply them again::

    python manage.py unmigrate --fake
    python manage.py migrate --fake


Contributing
------------

- Join the discussion at https://gitter.im/django-unmigrate/community.
- PRs are welcome! If you have questions or comments, please use the link
  above.
- To run the test suite run ``make`` or ``make coverage``. The tests for this
  project live inside a small django project called ``dunm_sandbox``. Beware!
  This package uses Git to function, therefore, the tests expect a number of
  commit hashes inside this repository to remain stable in order to function.
  See `this meta file`_ for further details.

.. _this meta file: dunm_sandbox/meta.py
