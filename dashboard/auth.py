from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class DashboardUserBackend(BaseBackend):
    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None

    def authenticate(self, request, email_or_username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(Q(username=email_or_username) | Q(email=email_or_username))
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

