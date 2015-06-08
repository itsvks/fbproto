from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from django.views.generic.base import TemplateView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fbproto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
