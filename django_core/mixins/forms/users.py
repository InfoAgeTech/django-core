
class UserFormMixin(object):
    """Form mixin that puts the user on the form object."""

    def __init__(self, user=None, *args, **kwargs):
        if not hasattr(self, 'user'):
            if user is None:
                raise Exception('user is required for this form.')

            self.user = user

        super(UserFormMixin, self).__init__(*args, **kwargs)
