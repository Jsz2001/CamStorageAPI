from .models import UserData

class UserQuerySetMixin:
    user_field = "user"
    allow_staff_view = False

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        user = self.request.user
        if not user.is_authenticated:
            # For private user-owned models, anonymous should see nothing
            return qs.none()

        if (self.allow_staff_view and user.is_staff) or user.is_superuser:
            return qs

        return qs.filter(**{self.user_field: user})


class ProfileQuerySetMixin:
    allow_staff_view = False

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        user = self.request.user

        if not user.is_authenticated:
            return qs.none()

        # allow staff/superuser to view (if enabled), OR allow user to view their own profile
        if ((self.allow_staff_view and user.is_staff) or user.is_superuser or (user.username == self.kwargs.get("username"))):
            return qs

        return qs.none()

    