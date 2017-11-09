from django.test import TestCase, RequestFactory
from ahhost.models import PointSource, PointSourceData
import datetime as dt
from ahhost.views import data_add, data_update
from pprint import pprint

class RequestTestCase(TestCase):
    def test_data_add(self):
        factory = RequestFactory()
        parameters = {
            0:'test',
            1:"",
            2:"",
            3:"",
            4:"",
            5:"",
            6:"",
            7:"12",
            8:"12",
            9:"",
            10:"",
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
        print('first',ps.station.areaId)

    def test_data_update(self):
        self.test_data_add()
        factory = RequestFactory()
        parameters = {
            0:'test',
            1:"12333",
            2:"12",
            3:"12",
            4:"12",
            5:"12",
            6:"12",
            7:"12",
            8:"12",
            9:"",
            10:"",
            11:"12",
            12:"12",
            13:"12",
            14:"12",
            15:"12",
            16:"12",
            17:"12",
            18:"12",
            19: "2017-11-10"
        }
        request = factory.post('/data/update',parameters)
        response = data_update(request)
        ps = PointSourceData.objects.get(station__stationName='test')
        print('second',ps.station.areaId)
