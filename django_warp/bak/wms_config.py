### wms_config.py

# Load django-wms classes
from wms import maps, layers, views

# Load model with spatial field (Point, Polygon, MultiPolygon)
from warp.models import datasets

# Subclass the WmsLayer class and point it to a spatial model
# use WmsVectorLayer for vector data and WmsRasterLayer for rasters
class coverage(layers.WmsRasterLayer):
    model = datasets

# Subclass the WmsMap class and add the layer to it
class testWmsMap(maps.WmsMap):
    layer_classes = [ coverage ]

# Subclass the WmsView to create a view for the map
class testWmsView(views.WmsView):
    map_class = testWmsMap