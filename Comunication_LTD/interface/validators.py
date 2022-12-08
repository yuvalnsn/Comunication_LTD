from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from interface.models import CustomUserPasswordHistory


class DontRepeatValidator:
    def __init__(self, history=2):
        self.history = history

    def validate(self, password, user=None):
        for last_pass in self._get_last_passwords(user):
            if check_password(password=password, encoded=last_pass):
                self._raise_validation_error()

    def get_help_text(self):
        return _("You cannot repeat passwords")

    def _raise_validation_error(self):
        raise ValidationError(
            _("This password has been used before."),
            code='password_has_been_used',
            params={'history': self.history},
        )

    def _get_last_passwords(self, user):
        all_history_user_passwords = CustomUserPasswordHistory.objects.filter(username_id=user).order_by('id')
        to_index = all_history_user_passwords.count() - self.history
        to_index = to_index if to_index > 0 else None
        if to_index:
            [u.delete() for u in all_history_user_passwords[0:to_index]]
        return [p.old_pass for p in all_history_user_passwords[to_index:]]
