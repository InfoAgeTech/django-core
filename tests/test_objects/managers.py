from django_core.db.models import SlugManager
from django_core.db.models import TokenManager
from django_core.db.models import UserManager
from django_core.db.models import CommonManager


class BaseTestManager(SlugManager, TokenManager, UserManager, CommonManager):
    pass
