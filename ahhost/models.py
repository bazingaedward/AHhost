from django.db import models

class PointSource(models.Model):
    "站点信息"
    # 单位名称(stationName)
    stationName = models.CharField(max_length=200, primary_key=True, unique=True)
    # 行政区划代码(areaId)
    areaId = models.CharField(max_length=10)
    # 省份(province)
    province = models.CharField(max_length=20)
    # 城市(city)
    city = models.CharField(max_length=30)
    # 区县(county)
    county = models.CharField(max_length=30)
    # 街道(street)
    street = models.CharField(max_length=50)
    # 地址(address)
    address = models.CharField(max_length=200)
    # 经度(longitude)
    longitude = models.FloatField()
    # 纬度(latitude)
    latitude = models.FloatField()
    # 行业类别代码(industryId)
    industryId = models.CharField(max_length=10)
    # 行业类别名称(industryName)
    industryName = models.CharField(max_length=30)

class PointSourceData(models.Model):
    "站点监测数据"
    station = models.ForeignKey(PointSource, on_delete=models.CASCADE)
    # 总量SO2(SO2)
    SO2 = models.FloatField(null=True)
    # 总量NOx(NOX)
    NOX = models.FloatField()
    # 总量CO(CO)
    CO = models.FloatField()
    # 总量PM(PM)
    PM = models.FloatField()
    # 总量PM10(PM10)
    PM10 = models.FloatField()
    # 总量PM2.5(PM25)
    PM25 = models.FloatField()
    # 总量NMVOC(NMVOC)
    NMVOC = models.FloatField()
    # 总量NH3(NH3)
    NH3 = models.FloatField()
    # 统计时间(date:2015.11)
    date = models.DateField()


class City(models.Model):
    "地级市"
    # ID:统一数字编码，例如：合肥市 340100
    ID = models.CharField(max_length=50, primary_key=True, unique=True)
    # name:名称
    name = models.CharField(max_length=50)
    # minx: 经度左边界
    minx = models.FloatField()
    # miny: 纬度下边界
    miny = models.FloatField()
    # maxx: 经度右边界
    maxx = models.FloatField()
    # maxy: 纬度上边界
    maxy = models.FloatField()

class Province(models.Model):
    "中国省级单位"
    # name:名称
    name = models.CharField(max_length=50, primary_key=True, unique=True)
    # minx: 经度左边界
    minx = models.FloatField()
    # miny: 纬度下边界
    miny = models.FloatField()
    # maxx: 经度右边界
    maxx = models.FloatField()
    # maxy: 纬度上边界
    maxy = models.FloatField()
