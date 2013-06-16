from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from inventory.views import showLastInventory, updateInventory,recordOrder
from inventory.views import orderHistory, inventoryHistory,startingInventory, notes, addNote
from inventory.views import recordDelivery, reportList, report, dailyReport
from inventory.views import latestInventories, latestOrders, unfilledOrders
from inventory.views import csvTotal, csvDailyReport
from inventory.views import tokensCollected, tokensDelivered
from inventory.views import recordTokenDelivery, recordTokenCollection
from inventory.views import addLocationTokenNote, addBoothTokenNote
from inventory.views import locationTokenNote, boothTokenNote, addBoothTokenNote, addLocationTokenNote
from inventory.views import collectionReport, deliveryReport, reconciliationReport
from inventory.views import csvCollectionReport,csvDeliveryReport, csvReconciliationReport
from inventory.views import showDashboardInventory, showDashboardOrders, showDashboardNotes, showVendorDashboard
urlpatterns = patterns('',
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    #dashboard URLs
    url(r'^dashboard/inventory', showDashboardInventory),
    url(r'^dashboard/orders', showDashboardOrders),
    url(r'^dashboard/notes', showDashboardNotes),
    #vandor dashboard
    url(r'^dashboard/vendors', showVendorDashboard),
    #regular old URLs
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
    url(r'^report/latest-inventories', latestInventories),
    url(r'^report/latest-orders', latestOrders),
    url(r'^report/unfilled-orders', unfilledOrders),
    #url(r'^report/latest-notes', latestNotes),
    url(r'^csv/report/total', csvTotal),
    url(r'^csv/report/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',csvDailyReport),
    url(r'^token/booth/(?P<location_number>[^\.]+)$', tokensDelivered),
    url(r'^token/location/(?P<location_number>[^\.]+)$', tokensCollected),
    url(r'^token/record-delivery/(?P<location_number>[^\.]+)$', recordTokenDelivery),
    url(r'^token/record-collection/(?P<location_number>[^\.]+)$', recordTokenCollection),
    url(r'^token/note/location/(?P<location_number>[^\.]+)$',locationTokenNote),
    url(r'^token/note/booth/(?P<location_number>[^\.]+)$', boothTokenNote),
    url(r'^token/add-note/location/(?P<location_number>[^\.]+)$',addLocationTokenNote),
    url(r'^token/add-note/booth/(?P<location_number>[^\.]+)$', addBoothTokenNote),
    url(r'^token/report/collection', collectionReport),
    url(r'^token/report/delivery', deliveryReport),
    url(r'^token/report/reconciliation', reconciliationReport),
    url(r'^csv/token/report/collection', csvCollectionReport),
    url(r'^csv/token/report/delivery', csvDeliveryReport),
    url(r'^csv/token/report/reconciliation', csvReconciliationReport),
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
