==============
DJANGO WARP
==============

.. image:: https://img.shields.io/pypi/v/django-warp.svg?style=plastic
    :target: https://pypi.python.org/pypi/django-warp/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/dm/django-warp.svg?style=plastic
    :target: https://pypi.python.org/pypi/django-warp/
    :alt: Downloads

.. image:: https://img.shields.io/pypi/l/django-warp.svg?style=plastic
    :target: https://pypi.python.org/pypi/django-warp/
    :alt: License

.. image:: https://img.shields.io/pypi/wheel/django-warp.svg?style=plastic
    :target: https://pypi.python.org/pypi/django-warp/
    :alt: Wheel Status

.. image:: https://img.shields.io/pypi/pyversions/django-warp.svg?style=plastic
    :target: https://pypi.python.org/pypi/django-warp/
    :alt: Supported Python Versions

Django Warp provides a reusable app for raster maps georeferencing.

Features
--------

* Many datasets with different settings, coordinate systems and basemaps.
* make use of GDAL/OGR library.
* Requires no Gis/desktop skills:
    * simple control input
    * visual feedback
* responsive interface

==============
REQUIREMENTS
==============

Required python libraries:

* django==1.9
* django-apps
* django-cors-headers
* django-http-proxy
* python-slugify
* django-imagekit
* django-raster==0.6
* pygdal==2.1.3.3

Required libraries:
GDAL/OGR 2.0 http://www.gdal.org/

==============
INSTALL
==============

Last stable version:

::

    pip install django-warp


Development version:

::

    pip install django-warp


=====
USAGE
=====

* Add ``django.contrib.gis``, ``httpproxy``, ``django_warp`` to your ``INSTALLED_APPS``
* Define ``MEDIA_URL``, ``MEDIA_ROOT``, ``STATIC_URL``, ``STATIC_ROOT``
* Add  ``url(r'^warp/', include('django_warp.urls')),`` to urlpatterns in site ``urls.py``
* Append ``+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`` to urlpatterns. A minimal ``urls.py`` should be like this:

::

    from django.conf.urls import include,url
    from django.conf.urls.static import static
    from django.conf import settings

    urlpatterns = [
        ...
        url(r'^warp/', include('django_warp.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

* ``./manage.py makemigrations django_warp`` and ``./manage.py migrate`` to create db context
* Run server and browse to ``[yourserver address]\warp\`` and login with a valid site credentials
* First create a dataset with epsg code, extents and baselayer
* Then upload images and define correlation and clipping to do georeferencing

=====
CHANGELOG
=====

0.1 first release

0.2 improved dataset manager

0.3 setting epsg projection different from 3857 4326 issues fix

0.4 new feature - download zipped collection of dataset georefs tiff along with .vrt file
new feature - auto pan/zoom on target/source view change
can't clip raster issue fixed

0.5 new feature - imagewms server for georeferenced datasets
new feature - display dataset coverage with internal imagewms server
new feature - overlay of all georeferenced datasets coverage from internal imagewms server in warp view
new feature - raster metadata edit in warp view
new feature - can move rasters between datasets
new feature - datasets cloning
accidental clipping polygon moving while panning in warp windows issue fixed
border transparency in datasets coverage issue fixed

=====
SCREENSHOTS
=====

available datasets

.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/datasets.png

dataset setting, default to EPSG:3857 projection (web mercator) and OSM baselayer

.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/dataset_form_3857.png

dataset custom settins: EPSG:3003 projection (web mercator) with ArcGis Mapserver baselayer

.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/dataset_form_3003.png

loading a new image

.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/image_load.png

correlated available images in datasets

.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/dataset_images.png

correlating source image on the left on target map on the right

.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/correlate_01.png

couple of correlation point on source image and target map

.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/correlate_02.png

clipping source image

.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/correlate_04.png

succesful correlation

.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/correlate_05.png

datasets coverage overlays in target map

.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/dataset_coverages.png

dataset overview with georeferenced images mosaic

.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/overview.png

printing a correlated image

.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/print.png

