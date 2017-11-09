from django.test import TestCase, RequestFactory
from ahhost.models import PointSource, PointSourceData
import datetime as dt
from ahhost.views import data_add

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
        }
        request = factory.post('/data/add',parameters)
        response = data_add(request)
        print(PointSource.objects.filter(stationName='test'))
        print(response)
