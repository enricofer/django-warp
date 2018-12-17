import os
from setuptools import find_packages, setup

import sys
if sys.version_info[0] < 3:
    print ("This package does not support Python 2.")
    sys.exit(1)

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-warp',
    version='0.6',
    packages=find_packages(),
    install_requires=[
        'Django>=1.11',
        'psycopg2',
        'django-cors-headers',
        'django-http-proxy',
        'python-slugify',
        'django-imagekit',
        'django-raster>=0.6',
        'requests',
        'GDAL>=2.1.0'
    ],
    include_package_data=True,
    license='GNU General Public License v3 (GPLv3)',  # example license
    description='A Django app for easy/collaborative georeferencing of raster datasets. Acts as web interface to GDAL/OGR',
    url='https://github.com/enricofer/django-warp',
    author='Enrico Ferreguti',
    author_email='enricofer@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',  # replace "X.Y" as appropriate
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
