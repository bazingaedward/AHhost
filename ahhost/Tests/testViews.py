from django.test import TestCase
from ahhost.models import PointSource
from ahhost.DataHandler import DataHandler
import datetime as dt
from django.test import Client

class ViewsTestCase(TestCase):
    def test_data_import(self):
        c = Client()
        response = c.get('/data/load')
        print(response.content)
