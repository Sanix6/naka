# tokens.py
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator


class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    timeout = 900 

    def is_token_expired(self, token):
        try:
            ts_b36 = token.split('-')[1]
            ts = self._base36_to_int(ts_b36)
        except Exception:
            return True

        now_ts = self._num_seconds(self._now())
        return (now_ts - ts) > self.timeout

custom_token_generator = CustomPasswordResetTokenGenerator()
