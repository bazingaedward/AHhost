from django.test import TestCase
from ahhost.Gridding import ShapeFileHandler,NCHandler,RasterHandler
from pprint import pprint

class GriddingTestCase(TestCase):
    def test_shape_file(self):
        # sfh = ShapeFileHandler([3137847.7813,845398.494453,3807148.73217,1425996.90967], \
        #     resolution=100000)
        sfh = ShapeFileHandler([28.949517145902025,112.7214002962958,35.06114891777644,121.73919504342172], \
            resolution=0.1)
        sfh.export('media/shapefiles/grid')

    def test_raster_handler(self):
        vector = 'media/shapefiles/grid.shp'
        raster = 'media/Population/AH/2010.tif'
        rh = RasterHandler(raster, vector)
        rh.process()
        result = rh.normalized()
        rh.export_geojson('media/geojson/data.geojson')
        return result

    def test_nc_handler(self):
        nh = NCHandler(self.test_raster_handler(), 'media/netcdf4/data.nc')
        resolution = float(10)/100.0
        pollution = {
            'name': 'SO2',
            'quantity': float(100)
        }
        nh.process('AH', pollution, resolution)
