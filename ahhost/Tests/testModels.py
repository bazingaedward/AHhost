from django.test import TestCase
from ahhost.models import PointSource, City
from ahhost.DataHandler import DataHandler
from ahhost.view.province import saveToORM
import datetime as dt

class PointSourceTestCase(TestCase):
    def test_data_import(self):
        point = PointSource(
            stationName = '安徽省水泥制品有限公司',
            # 行政区划代码(areaId)
            areaId = '340102',
            # 省份(province)
            province = '安徽省',
            # 城市(city)
            city = '合肥市',
            # 区县(county)
            county = '瑶海区',
            # 街道(street)
            street = '',
            # 地址(address)
            address = '2',
            # 经度(longitude)
            longitude = 117.338255,
            # 纬度(latitude)
            latitude = 31.889577,
            # 行业类别代码(industryId)
            industryId = '3021',
            # 行业类别名称(industryName)
            industryName = '水泥制品制造',
            # 总量SO2(SO2)
            SO2 = 9.6,
            # 总量NOx(NOX)
            NOX = 4.836,
            # 总量CO(CO)
            CO = 7.28,
            # 总量PM(PM)
            PM = 8.43266708,
            # 总量PM10(PM10)
            PM10 = 1.939513428,
            # 总量PM2.5(PM25)
            PM25 = 0.505960025,
            # 总量NMVOC(NMVOC)
            NMVOC = 0.216,
            # 总量NH3(NH3)
            NH3 = 0.000336,
            # 统计时间(date:2015.11)
            date = dt.datetime.now()
        )
        point.save()
        point2 = PointSource.objects.all()
        print(point2)

    # def test_get_data(self):
        point = PointSource.objects.get(stationName = '安徽省水泥制品有限公司')
        print(point.areaId)

    def test_data_handler(self):
        COL = [
            'stationName',
            'areaId',
            'province',
            'city',
            'county',
            'street',
            'address',
            'longitude',
            'latitude',
            'industryId',
            'industryName',
            'SO2',
            'NOX',
            'CO',
            'PM',
            'PM10',
            'PM25',
            'NMVOC',
            'NH3'
            ]
        dh = DataHandler()
        # print(dh.engine)
        df = dh.loadExcel('media/安徽省排放清单估算结果-2015.11.xlsx')
        df2 = df.ix[:, :19]
        df2.columns = COL
        dh.saveToORM(df2, dt.date(2015, 11, 1))
        if PointSource.objects.filter(stationName='安徽安能热电股份有限公司'):
            print(True)
        else:
            print(False)
        # dh.saveToDB(df2, 'ahhost.pointsource', exist_action='replace')

class CityTestCase(TestCase):
    def test_data_import(self):
        saveToORM('hello')

class ProvinceTestCase(TestCase):
    def test_data_import(self):
        saveToORM('hello')
