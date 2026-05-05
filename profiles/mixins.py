from django.contrib.auth.mixins import UserPassesTestMixin


class RoleAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return bool(user.is_authenticated and getattr(user, "is_role_admin", False))
