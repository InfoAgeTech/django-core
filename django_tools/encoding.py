# -*- coding: utf-8 -*-
import hashlib

from django.utils.encoding import smart_str


def hash_secret(secret):
    h = hashlib.sha256()
    h.update(smart_str(secret))
    return h.hexdigest()
