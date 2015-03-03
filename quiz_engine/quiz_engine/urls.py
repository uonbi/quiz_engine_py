from django.conf.urls import patterns, include, url
from django.contrib import admin

from quiz_app.views import treasure_hunt

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'quiz_engine.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^codejamer/$', 'treasure_hunt' name = 'treasure_hunt'),
)
