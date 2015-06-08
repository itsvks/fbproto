from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from accounts.models import Profile, FriendList, FriendRequestSent, FriendRequestReceived, ProfileImage


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, max_length=100)
    last_name = serializers.CharField(required=True, max_length=100)
    email = serializers.EmailField(required=True, max_length=100)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'username')
        read_only_fields = ('username',)
        write_only_fields = ('password',)

    def restore_object(self, attrs, instance=None):
        """hack for pwdValidationError
        """

        assert instance is None, 'Cannot update users with RegisterSerializer'
        user = User(**attrs)
        user.set_password(attrs['password'])
        return user

    def validate_email(self, attrs, source):
        email = attrs[source]
        if email and User.objects.filter(email=email).count():
            raise serializers.ValidationError("Email Already Exist")
        else:
            return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=128)


class TokenSerializer(serializers.Serializer):
    class Meta:
        model = Token
        fields = ('key',)


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.Field(source='owner.first_name')
    last_name = serializers.Field(source='owner.last_name')
    email = serializers.Field(source='owner.email'  )

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'age', 'current_city',
                  'home_town', 'workplace', 'college', 'mobile_number', 'relationship',)


class ProfileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('age', 'current_city', 'home_town', 'workplace', 'college',
                  'mobile_number', 'relationship',)


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = ('image',)


class FriendRequestSentSerializer(serializers.ModelSerializer):
    first_name = serializers.Field(source='friend_request.first_name')

    class Meta:
        model = FriendRequestSent
        fields = ('friend_request', 'first_name',)


class FriendRequestReceivedSerializer(serializers.ModelSerializer):
    first_name = serializers.Field(source='friend_request.first_name')

    class Meta:
        model = FriendRequestReceived
        fields = ('friend_request', 'first_name',)


class SearchFriendSerializer(serializers.ModelSerializer):
    profile_image = ProfileImageSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'profile_image',)


class AddFriendSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequestSent
        fields = ('friend_request',)


class FriendRequestAcceptSerializer(serializers.Serializer):
    friend_request = serializers.IntegerField()


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    profile_image = ProfileImageSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'profile', 'profile_image',)


class UnFriendSerializer(serializers.Serializer):
    friend_id = serializers.IntegerField()