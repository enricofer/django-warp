==============
Django Warp
==============

Django Warp provides a reusable app for georeferencing of raster maps.

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
* psycopg2
* django-apps
* django-cors-headers
* django-http-proxy
* python-slugify
* django-imagekit
* git+https://github.com/geodesign/django-raster.git@master (development version)






==============
INSTALL
==============

Last stable version:

::

    pip install django-warp



=====
USAGE
=====

* Add ``django_warp`` to your ``INSTALLED_APPS``
