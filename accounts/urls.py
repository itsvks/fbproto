from accounts import views
from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static


urlpatterns = patterns('',
                       url(r'^register/$', views.Register.as_view(), name='register'),
                       url(r'^login/$', views.Login.as_view(), name='login'),
                       url(r'^logout/$', views.Logout.as_view(), name='logout'),
                       url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
                       url(r'^profile-image/$', views.ProfileImageView.as_view(), name='profile-image'),
                       url(r'^search-friend/(?P<q>.+)/$', views.SearchFriend.as_view(), name='search-friend'),
                       url(r'^user-detail/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
                       url(r'^add-friend/$', views.AddFriendView.as_view(), name='add-friend'),
                       url(r'^un-friend/(?P<pk>[0-9]+)/$', views.UnFriendView.as_view(), name='un-friend'),
                       url(r'^friend-list/$', views.FriendListView.as_view(), name='friend-list'),
                       url(r'^friend-request-sent/$', views.FriendRequestSentView.as_view(), name='friend-request-sent'),
                       url(r'^friend-request-received/$', views.FriendRequestReceivedView.as_view(),
                           name='friend-request-received'),
                       url(r'^friend-request-accept/$', views.FriendRequestAcceptView.as_view(),
                           name='friend-request-accept'),
                       )

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
