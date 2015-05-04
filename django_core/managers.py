from __future__ import unicode_literals

from datetime import datetime

from .db.models.managers import CommonManager
from .db.models.managers import TokenManager


class TokenAuthorizationManager(TokenManager, CommonManager):
    """Model manager for token authorizations."""

    def expire_by_email(self, email_address, reason, **kwargs):
        """Expires tokens for an email address or email addresses.

        :param email_address: the string email address or emails addresses to
            expire tokens for.
        :param reason: the codified reason for the tokens.  If explicitly set
            to None, this will expire all tokens for the email provided.
        """
        if email_address is None:
            # no email(s) provided.  Nothing to do.
            return None

        if isinstance(email_address, (list, tuple)):
            kwargs['email_address__in'] = email_address
        else:
            kwargs['email_address'] = email_address

        if reason is not None:
            kwargs['reason'] = reason

        self.filter(**kwargs).update(expires=datetime(1970, 1, 1))

    def expire_by_emails(self, email_addresses, reason, **kwargs):
        """Expires tokens by a list of email addresses."""
        self.expire_by_email(email_address=email_addresses,
                             reason=reason,
                             **kwargs)
