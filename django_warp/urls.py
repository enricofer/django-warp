from django.conf.urls import url,include
from . import views
#from warp.wms_config import testWmsView
from httpproxy.views import HttpProxy
#from revproxy.views import ProxyView
from django.conf import settings
import django.contrib.auth.views

urlpatterns = [
    url(r'^$', views.datasets_list, name='datasets_list'),
    url(r'^(\d+)/$', views.dataset_list, name='dataset_list'),
    url(r'^newdataset/$', views.dataset_form, name='dataset_new'),
    url(r'^removedataset/(\d+)/$', views.remove_dataset, name='dataset_remove'),
    url(r'^updateimage/$', views.update_image, name='dataset_remove'),
    url(r'^emptytrash/$', views.empty_trash, name='empty_trash'),
    url(r'^vrtdataset/(\d+)/$', views.vrt_dataset, name='dataset_vrt'),
    url(r'^download_dataset/(\d+)/$', views.download_dataset, name='dataset_download'),
    url(r'^clone_dataset/(\d+)/$', views.clone_dataset, name='dataset_clone'),
    url(r'^editdataset/(?P<datasetId>\d+)/$', views.dataset_form, name='dataset_form'),
    url(r'^viewdataset/(?P<datasetId>\d+)/$', views.dataset_view, name='dataset_view'),
    url(r'^newimage/(?P<datasetId>\d+)/$', views.georef_start, name='georef_new'),
    url(r'^trashimage/(\d+)/$', views.trash_image, name='georef_trash'),
    url(r'^recoverimage/(\d+)/$', views.recover_image, name='georef_recover'),
    url(r'^imgset/(?P<idx>\d+)/$', views.georef_start, name='georef_start'),
    url(r'^apply/$', views.georef_apply, name='georef_apply'),
    url(r'^print/(\d+)/$', views.georef_print, name='georef_print'),
    url(r'^proxy/(?P<url>.*)', HttpProxy.as_view(base_url="")),
    url(r'^export/$', views.export, name='export'),
    #url(r'^proxy/(?P<path>.*)', ProxyView.as_view(upstream='https://')),
    url(r'^login/', django.contrib.auth.views.login),
    url(r'^logout/', django.contrib.auth.views.logout),
    #url(r'raster/', include('raster.urls')),
    #url(r'^wms/$', testWmsView.as_view(), name='wms'),
]
