from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    owner = models.ForeignKey(User, unique=True, related_name='profile')
    age = models.CharField(max_length=3)
    current_city = models.CharField(max_length=255, blank=True, null=True)
    home_town = models.CharField(max_length=255, blank=True, null=True)
    workplace = models.CharField(max_length=255, blank=True, null=True)
    college = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=255, blank=True, null=True)
    relationship = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.age


def profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = 'user_id_' + str(instance.owner.id) + '.' + ext
    return '/'.join(['accounts/profile-image', str(instance.owner.id), filename])


class ProfileImage(models.Model):
    owner = models.ForeignKey(User, unique=True, related_name='profile_image')
    image = models.ImageField(upload_to=profile_image_path, blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.image


class FriendList(models.Model):
    friend1 = models.ForeignKey(User, related_name='friend1')
    friend2 = models.ForeignKey(User, related_name='friend2')
    is_friend = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" % self.friend1


class FriendRequestSent(models.Model):
    owner = models.ForeignKey(User)
    friend_request = models.ForeignKey(User, related_name='friend_request_sent')
    is_accepted = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % self.friend_request


class FriendRequestReceived(models.Model):
    owner = models.ForeignKey(User)
    friend_request = models.ForeignKey(User, related_name='friend_request_received')
    is_accepted = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % self.friend_request