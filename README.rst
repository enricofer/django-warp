==============
Django Warp
==============

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
* Add  ``url(r'^warp/', include('django_warp.urls')),`` to site ``urls.py``
* ``./manage.py makemigrations django_warp`` and ``./manage.py migrate`` to create db context
* Run server and browse to ``[yourserver address]\warp\`` and login with a valid site credentials
* First create a dataset with epsg code, extents and baselayer
* Then upload images and define correlation and clipping to do georeferencing

=====
SCREENSHOTS
=====

.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/datasets.png
.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/dataset_form_3857.png
.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/dataset_form_3003.png
.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/image_load.png
.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/dataset_images.png
.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/correlate_01.png
.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/correlate_02.png
.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/correlate_04.png
.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/correlate_05.png
.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/overview.png
.. image:: https://raw.githubusercontent.com/enricofer/django-warp/master/docs/print.png
