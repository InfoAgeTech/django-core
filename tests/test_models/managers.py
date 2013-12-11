from django_core.managers import SlugManager
from django_core.managers import TokenManager
from django_core.managers import UserManager
from django_core.managers import CommonManager


class BaseTestManager(SlugManager, TokenManager, UserManager, CommonManager):
    pass
