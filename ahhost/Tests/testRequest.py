from django.test import TestCase, RequestFactory
from ahhost.models import PointSource, PointSourceData
import datetime as dt
from ahhost.view.data import data_add, data_update, data_filter, data_geojson
from ahhost.views import raster_calculate, interpolate
from ahhost.view import province
from pprint import pprint

class RequestTestCase(TestCase):
    def test_data_add(self):
        factory = RequestFactory()
        parameters = {
            0:'test',
            1:"hello",
            2:"",
            3:"",
            4:"",
            5:"",
            6:"",
            7:"12",
            8:"12",
            9:"",
            10:"industry",
            11:"12",
            12:"12",
            13:"12",
            14:"12",
            15:"12",
            16:"12",
            17:"12",
            18:"12",
            19: "2017-11-09"
        }
        request = factory.post('/data/add',parameters)
        response = data_add(request)
        ps = PointSourceData.objects.get(station__stationName='test')
        print('first--------------')
        print(ps.station.stationName,ps.station.areaId,ps.station.industryName,ps.date)

    def test_data_update(self):
        self.test_data_add()
        factory = RequestFactory()
        parameters = {
            0:'test',
            1:"world",
            2:"12",
            3:"12",
            4:"12",
            5:"12",
            6:"12",
            7:"12",
            8:"12",
            9:"",
            10:"name",
            11:"12",
            12:"12",
            13:"12",
            14:"12",
            15:"12",
            16:"12",
            17:"12",
            18:"12",
            19: "2017-11-10",
        }
        request = factory.post('/data/update',parameters)
        response = data_update(request)
        ps = PointSourceData.objects.get(station__stationName='test')
        print('second--------------')
        print(ps.station.stationName,ps.station.areaId,ps.station.industryName,ps.date)

    def test_data_filter(self):
        factory = RequestFactory()
        parameters = {
          'sql': "SO2 > 1000"
        }
        request = factory.post('/data/filter',parameters)
        response = data_filter(request)
        print(response)

    def test_dataframe_sum(self):
        import pandas as pd
        data = [
            ['hello', '12', '4'],
            ['world', '13', '5.0']
            ]
        df = pd.DataFrame(data)
        total = df[[1,2]].astype(float).sum(numeric_only=True).as_matrix()
        print(total)

    def test_data_geojson(self):
        factory = RequestFactory()
        parameters = {}
        request = factory.post('/data/geojson',parameters)
        response = data_geojson(request)
        print(response)

    def test_gis_province_get(self):
        factory = RequestFactory()
        parameters = {}
        request = factory.post('/gis/province/save',parameters)
        province.saveToORM(request)
        request = factory.post('/gis/province/get',parameters)
        response = province.getAll(request)
        print(response)

    def raster_calculate(self):
        factory = RequestFactory()
        parameters = {
            'Area': 'AH',
            'st'  : 'Population',
            'resolution': '50',
            'type': 'so2',
            'sum': '100',
        }
        request = factory.post('/form/raster',parameters)
        response = raster_calculate(request)
        print(response)

    def interpolate(self):
        factory = RequestFactory()
        parameters = {
            'var':'["SO2", "NOX"]',
            'resolution': 100,
            'method': 'linear'
        }
        request = factory.post('/form/interpolate',parameters)
        response = interpolate(request)
        pprint(response)
