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

.. image:: https://badge.fury.io/py/django-unmigrate.svg
    :alt: PyPi version
    :target: http://badge.fury.io/py/django-unmigrate

.. image:: https://img.shields.io/pypi/dm/django-unmigrate
    :alt: Downloads

|

If you are in a complex Django project, sometimes you will find yourself switching
between multiple branches, each of which adds a number of database migrations.
Before switching back to the ``master`` branch you will have to unapply all
migrations that are specific to the current branch. To make things worse, in
order to unapply Django migrations, you have to enter the migration that comes
right before the first migration that the current branch introduces.

With django-unmigrate, you don't need to worry about that anymore. Standing on
any branch, you can use::

    python manage.py unmigrate master

And that's it!

Contributing
------------

- Join the discussion at https://gitter.im/django-unmigrate/community.
- PRs are welcome! If you have questions or comments, please use the link
  above.
