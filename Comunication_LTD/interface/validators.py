from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from interface.models import CustomUserPasswordHistory
from config import sec_lvl

import re

class DontRepeatValidator:
    def __init__(self, history=2):
        self.history = history

    def validate(self, password, user=None):
        last_history_passwords = self._get_last_passwords(user)

        print(last_history_passwords)

        for password_history in last_history_passwords:
            if sec_lvl == 'high' and check_password(password=password, encoded=password_history) or sec_lvl == 'low' and password == password_history:
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
        length = len(all_history_user_passwords)

        last_history_passwords = [password.old_pass for password in all_history_user_passwords[max(length - self.history, 0):]]

        return last_history_passwords

class PatternValidator:
    def __init__(self, pattern):
        self.pattern = pattern
    def validate(self, password, user = None):
        matched = re.match(self.pattern, password)

        if not bool(matched):
            self._raise_validation_error()
    def _raise_validation_error(self):
        raise ValidationError(
            _("Your password does not meet the requirements"),
            code='password_has_been_used',
            params={'pattern': self.pattern},
        )
    def get_help_text(self):
        return _("Your password does not meet the requirements")
