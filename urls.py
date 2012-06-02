from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from inventory.views import showLastInventory, updateInventory, test, recordOrder
from inventory.views import orderHistory, inventoryHistory,startingInventory, notes, addNote
from inventory.views import recordDelivery, reportList, report, dailyReport

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'irishfest.views.home', name='home'),
    # url(r'^irishfest/', include('irishfest.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^location/(?P<location_number>[^\.]+)$', showLastInventory),
    url(r'^update-inventory/(?P<location_number>[^\.]+)$', updateInventory),
    url(r'^order-history/(?P<location_number>[^\.]+)$', orderHistory),
    url(r'^inventory-history/(?P<location_number>[^\.]+)$', inventoryHistory),
    url(r'^starting-inventory/(?P<location_number>[^\.]+)$', startingInventory),
    url(r'^notes/(?P<location_number>[^\.]+)$', notes),
    url(r'^add-note/(?P<location_number>[^\.]+)$', addNote),
    url(r'^record-order/(?P<location_number>[^\.]+)$', recordOrder),
    url(r'^record-delivery/(?P<location_number>[^\.]+)/(?P<order_id>[^\.]+)/(?P<order_delivered>[^\.]+)$', recordDelivery),
    url(r'^report/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',dailyReport),
    url(r'^report/total', report),
    url(r'^report-list/', reportList),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )


if settings.DEBUG:
    urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
    ) 
