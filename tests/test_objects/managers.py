from django_core.models.managers import SlugManager
from django_core.models.managers import TokenManager
from django_core.models.managers import UserManager
from django_core.models.managers import CommonManager


class BaseTestManager(SlugManager, TokenManager, UserManager, CommonManager):
    pass
