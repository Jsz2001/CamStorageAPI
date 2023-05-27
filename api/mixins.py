from .models import UserData

class UserQuerySetMixin():
    user_field ='user'
    allow_staff_view = False

    def get_queryset(self, *args, **kwargs):       
        if not self.request.user.id:
            self.request.user = UserData.object.get(username='Example')
        user = self.request.user        
        lookup_data = {}
        lookup_data[self.user_field] = user

        qs = super().get_queryset(*args, **kwargs)
        if (self.allow_staff_view and user.is_staff) | user.is_superuser:
            return qs
        return qs.filter(**lookup_data)

    
    
class ProfileQuerySetMixin():
    user_field = 'user'
    allow_staff_view = False

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
    
        qs = super().get_queryset(*args, **kwargs)
        if (self.allow_staff_view and user.is_staff) | user.is_superuser | (user.username==self.kwargs['username']):
            return qs
        return None
    