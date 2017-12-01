from django.test import TestCase
from ahhost.Interpolation import PointSourceInterpolation as PSI
from pprint import pprint
# from ahhost.models import Province, City
from ahhost.view import province, city

class Interpolate(TestCase):
    def init(self):
        psi = PSI()

    def process(self):
        province.saveToORM('hello')
        province.saveToORM('hello')
        psi = PSI()
