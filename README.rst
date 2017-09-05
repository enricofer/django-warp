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
* psycopg2
* django-apps
* django-cors-headers
* django-http-proxy
* python-slugify
* django-imagekit
* git+https://github.com/geodesign/django-raster.git@master (development version)

Required libraries:
GDAL/OGR r 2 http://www.gdal.org/

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

* Add ``django_warp`` to your ``INSTALLED_APPS``
* Add  ``url(r'^warp/', include('django_warp.urls')),`` to site ``urls.py``
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

dataset overview with georeferenced images mosaic

.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/overview.png

printing a correlated image

.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/print.png

