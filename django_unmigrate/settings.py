from django.conf import settings

MAIN_BRANCH = getattr(settings, "MAIN_BRANCH", "master")
