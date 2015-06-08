from random import choice
from string import letters

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q
from django.http.response import Http404
from django.utils import timezone
from rest_framework import permissions, status, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile, FriendRequestSent, FriendList, FriendRequestReceived, ProfileImage
from accounts.serializers import RegisterSerializer, LoginSerializer, TokenSerializer, ProfileSerializer, \
    FriendRequestSentSerializer, FriendRequestReceivedSerializer, SearchFriendSerializer, \
    FriendRequestAcceptSerializer, AddFriendSerializer, UserSerializer, ProfileImageSerializer, ProfileCreateSerializer

# Create your views here.


class Register(generics.CreateAPIView):
    """
        Register a new user to system
    """

    serializer_class = RegisterSerializer
    model = User

    @staticmethod
    def get_random_username():
        random_username = ''.join([choice(letters) for i in xrange(30)])
        return random_username

    def post(self, request):
        first_name = request.DATA['first_name']
        last_name = request.DATA['last_name']

        serialized = self.serializer_class(data=request.DATA)
        if serialized.is_valid():
            user = User.objects.create_user(
                self.get_random_username(),
                serialized.init_data['email'],
                serialized.init_data['password'], )
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            Profile(owner=user).save()
            ProfileImage(owner=user).save()

            new_user = authenticate(email=serialized.init_data['email'],
                                    password=serialized.init_data['password'])
            login(request, new_user)

            token = Token.objects.get_or_create(user=user)[0].key
            return Response({'token': token,
                             'first_name': new_user.first_name,
                             'last_name': new_user.last_name},
                            status=status.HTTP_200_OK)

        else:
            return Response({'user': serialized.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class Login(generics.GenericAPIView):
    """
        Login a existing user to system
    """
    serializer_class = LoginSerializer
    token_model = Token
    token_serializer = TokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            user = authenticate(email=serializer.data['email'],
                                password=serializer.data['password'])
            if user and user.is_authenticated():
                if user.is_active:
                    #login(request, user)

                    token = self.token_model.objects.get_or_create(user=user)[0].key

                    # Update last login time
                    user.last_login = timezone.now()
                    user.save(update_fields=['last_login'])

                    return Response({'token': token,
                                     'first_name': user.first_name,
                                     'last_name': user.last_name},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'error': ['This account is disabled.']},
                                    status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': ['Invalid Username/Password.']},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    """
        Logout a logged in user to system
    """

    def get(self, request):
        try:
            logout(request)
            return Response({'success': 'Successfully logged out.'},
                            status=status.HTTP_200_OK)
        except Exception, e:
            print e
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    model = Profile
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    def pre_save(self, obj):
        obj.owner_id = self.request.user.id

    def post(self, request, *args, **kwargs):
        serializer = ProfileCreateSerializer(data=request.DATA)

        if serializer.is_valid():

            profile, created = self.model.objects.get_or_create(owner=self.request.user)
            profile.age = serializer.data['age']
            profile.college = serializer.data['college']
            profile.current_city = serializer.data['current_city']
            profile.home_town = serializer.data['home_town']
            profile.mobile_number = serializer.data['mobile_number']
            profile.relationship = serializer.data['relationship']
            profile.workplace = serializer.data['workplace']
            profile.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileImageView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    model = ProfileImage
    serializer_class = ProfileImageSerializer

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    def pre_save(self, obj):
        obj.owner_id = self.request.user.id

    def post(self, request, *args, **kwargs):
        profile_image, created = self.model.objects.get_or_create(owner=self.request.user)
        serializer = self.serializer_class(profile_image, data=request.DATA,
                                           files=request.FILES)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FriendListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    model = FriendList

    def get(self, request, format=None):
        friends1 = self.model.objects.filter(friend1=self.request.user, is_friend=True)
        friends2 = self.model.objects.filter(friend2=self.request.user, is_friend=True)
        l = []
        for result in friends1:
            l.append({'friend_id': result.friend2.id,
                      'friend_name': result.friend2.first_name})
        for result in friends2:
            l.append({'friend_id': result.friend1.id,
                      'friend_name': result.friend1.first_name})
        return Response(l)


class FriendRequestSentView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    model = FriendRequestSent
    serializer_class = FriendRequestSentSerializer

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user, is_accepted=False)


class FriendRequestReceivedView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    model = FriendRequestReceived
    serializer_class = FriendRequestReceivedSerializer

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user.id, is_accepted=False)


class FriendRequestAcceptView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    model = FriendList
    serializer_class = FriendRequestAcceptSerializer

    def pre_save(self, obj):
        obj.friend1 = self.request.user

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            frr = FriendRequestReceived.objects.filter(
                owner=self.request.user,
                friend_request=int(serializer.data['friend_request']),
                is_accepted=False)

            if len(frr) > 0:

                friend_list = FriendList.objects.filter(
                    Q(friend1=self.request.user, friend2=int(serializer.data['friend_request'])) |
                    Q(friend2=self.request.user, friend1=int(serializer.data['friend_request'])))

                if len(friend_list) > 0:
                    friend_list[0].is_friend = True
                    friend_list[0].save()
                else:
                    fl = FriendList(friend1=self.request.user,
                                    friend2=User.objects.get(pk=int(serializer.data['friend_request'])))
                    fl.save()

                FriendRequestReceived.objects.filter(
                    owner=self.request.user,
                    friend_request=int(serializer.data['friend_request']),
                    is_accepted=False).update(is_accepted=True)

                FriendRequestSent.objects.filter(
                    owner=User.objects.get(pk=int(serializer.data['friend_request'])),
                    friend_request=self.request.user).update(is_accepted=True)

                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': ['Wrong Friend Request id.']}, status=status.HTTP_401_UNAUTHORIZED)


class AddFriendView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddFriendSerializer
    model = FriendRequestSent

    def pre_save(self, obj):
        obj.owner = self.request.user

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            if int(serializer.data['friend_request']) is not request.user.id:
                friend_list = FriendList.objects.filter(
                    Q(friend1=self.request.user,
                      friend2=int(serializer.data['friend_request']),
                      is_friend=True) |
                    Q(friend2=self.request.user,
                      friend1=int(serializer.data['friend_request']),
                      is_friend=True))

                if len(friend_list) > 0:
                    return Response({'error': ['Friend Already Added.']},
                                    status=status.HTTP_401_UNAUTHORIZED)

                else:
                    frs = FriendRequestSent.objects.filter(
                        owner=self.request.user,
                        friend_request=int(serializer.data['friend_request']),
                        is_accepted=False)

                    frr = FriendRequestReceived.objects.filter(
                        owner=self.request.user,
                        friend_request=int(serializer.data['friend_request']),
                        is_accepted=False)

                    if len(frs) > 0 or len(frr) > 0:
                        return Response({'error': ['Friend Request Already Sent/Received.']},
                                        status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        self.pre_save(serializer.object)
                        serializer.save()
                        frr1 = FriendRequestReceived()
                        frr1.owner = User.objects.get(pk=int(serializer.data['friend_request']))
                        frr1.friend_request = self.request.user
                        frr1.save()
                        return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': ['Invalid Friend.']},
                                status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchFriend(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SearchFriendSerializer

    def get_queryset(self):
        q = self.kwargs['q']
        return User.objects.filter(
            Q(first_name__iexact=q) |
            Q(email__iexact=q)).exclude(id=self.request.user.id)


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    model = User

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = self.serializer_class(user)

        friend_list = FriendList.objects.filter(
            Q(friend1=self.request.user, friend2=pk, is_friend=True) |
            Q(friend2=self.request.user, friend1=pk, is_friend=True))

        frs = FriendRequestSent.objects.filter(
            owner=self.request.user,
            friend_request=pk,
            is_accepted=False)

        frr = FriendRequestReceived.objects.filter(
            owner=self.request.user,
            friend_request=pk,
            is_accepted=False)

        if int(pk) == int(request.user.id):
            serializer.data['is_owner'] = True
        else:
            serializer.data['is_owner'] = False
        if len(friend_list) > 0:
            serializer.data['is_friend'] = True
        else:
            serializer.data['is_friend'] = False
        if len(frs) > 0:
            serializer.data['is_friend_request_sent'] = True
        else:
            serializer.data['is_friend_request_sent'] = False
        if len(frr) > 0:
            serializer.data['is_friend_request_received'] = True
        else:
            serializer.data['is_friend_request_received'] = False

        return Response(serializer.data)


class UnFriendView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    model = FriendList

    def get_object(self, pk):
        try:
            return self.model.objects.get(
                Q(friend1=self.request.user, friend2=pk, is_friend=True) |
                Q(friend2=self.request.user, friend1=pk, is_friend=True)
            )

        except self.model.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        friend = self.get_object(pk)
        friend.is_friend = False
        friend.save()
        return Response(status=status.HTTP_204_NO_CONTENT)