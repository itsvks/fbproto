from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

# class EmailOrUsernameModelBackend(object):
#     def authenticate(self, username=None, password1=None):
#         if '@' in username:
#             kwargs = {'email': username}
#         else:
#             kwargs = {'username': username}
#         try:
#             user = User.objects.get(**kwargs)
#             if user.check_password(password1):
#                 return user
#         except User.DoesNotExist:
#             return None
# 
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None


class EmailAuthBackEnd(ModelBackend):
    def authenticate(self,email=None,password=None,**kwargs):
        try:
            user=User.objects.get(email=email)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None        