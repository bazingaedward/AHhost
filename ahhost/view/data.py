import os, json
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.db.models import Sum
from ahhost.models import PointSource, PointSourceData
from ahhost.DataHandler import DataHandler
import datetime as dt
from django_pandas.io import read_frame
from pprint import pprint
import pandas as pd
import geojson


def data_import(request, date='2015-11-01'):
    "导入Excel数据文件"
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
    df = dh.loadExcel('media/excel/data.xlsx')
    df2 = df.ix[:, :19]
    df2.columns = COL
    dh.saveToORM(df2, date)
    return HttpResponse('ok')

def data_load(request):
    "从数据库中提取污染源监测数据"
    data = []
    qs = PointSourceData.objects.all()
    for record in qs:
        data.append([
            record.station.stationName,
            record.station.areaId,
            record.station.province,
            record.station.city,
            record.station.county,
            record.station.street,
            record.station.address,
            "%.1f" %record.station.longitude,
            "%.1f" %record.station.latitude,
            record.station.industryId,
            record.station.industryName,
            "%.1f" %record.SO2,
            "%.1f" %record.NOX,
            "%.1f" %record.CO,
            "%.1f" %record.PM,
            "%.1f" %record.PM10,
            "%.1f" %record.PM25,
            "%.1f" %record.NMVOC,
            "%.1f" %record.NH3,
            record.date
            ])
    # df = read_frame(qs)
    # data = df[['station','SO2','NOX','CO','PM','PM10','PM25','NMVOC','NH3']]

    return JsonResponse({'data': data})
    # return JsonResponse({'data': df.to_json(orient='records')})

def data_filter(request):
    "数据过滤及分析"
    parameters = request.POST

    data = []
    qs = PointSourceData.objects.raw(
        '''
        select ahhost_pointsourcedata.* from ahhost_pointsourcedata
        join ahhost_pointsource on
        ahhost_pointsourcedata.station_id=ahhost_pointsource.stationName
        where %s
        ''' %parameters['sql'])
    for record in qs:
        data.append([
            record.station.stationName,
            record.station.areaId,
            "%.1f" %record.SO2,
            "%.1f" %record.NOX,
            "%.1f" %record.CO,
            "%.1f" %record.PM,
            "%.1f" %record.PM10,
            "%.1f" %record.PM25,
            "%.1f" %record.NMVOC,
            "%.1f" %record.NH3,
            record.date
            ])
    total = []
    if data:
        df = pd.DataFrame(data)
        total = df[[2,3,4,5,6,7,8,9]].astype(float).sum(numeric_only=True).to_json()
    return JsonResponse({'status': 'OK','data': data,'total':total})

def data_add(request):
    "数据库添加记录"
    parameters = request.POST
    station = PointSource(
        stationName = parameters['0'],
        areaId = parameters['1'],
        province = parameters['2'],
        city = parameters['3'],
        county = parameters['4'],
        street = parameters['5'],
        address = parameters['6'],
        longitude = parameters['7'],
        latitude = parameters['8'],
        industryId = parameters['9'],
        industryName = parameters['10'],
    )
    station.save()
    data = PointSourceData(
        station = station,
        SO2 = parameters['11'],
        NOX = parameters['12'],
        CO = parameters['13'],
        PM = parameters['14'],
        PM10 = parameters['15'],
        PM25 = parameters['16'],
        NMVOC = parameters['17'],
        NH3 = parameters['18'],
        date= parameters['19']
    )
    data.save()
    return JsonResponse({'status': 'OK'})

def data_update(request):
    "数据库更新记录"
    parameters = request.POST
    station = PointSource.objects.get(stationName=parameters['0'])
    # station.stationName = parameters['0']
    station.areaId = parameters['1']
    station.province = parameters['2']
    station.city = parameters['3']
    station.county = parameters['4']
    station.street = parameters['5']
    station.address = parameters['6']
    station.longitude = parameters['7']
    station.latitude = parameters['8']
    station.industryId = parameters['9']
    station.industryName = parameters['10']
    station.save()
    data = PointSourceData.objects.get(station__stationName=parameters['0'])
    data.SO2 = parameters['11']
    data.NOX = parameters['12']
    data.CO = parameters['13']
    data.PM = parameters['14']
    data.PM10 = parameters['15']
    data.PM25 = parameters['16']
    data.NMVOC = parameters['17']
    data.NH3 = parameters['18']
    data.date= parameters['19']
    data.save()
    return JsonResponse({'status': 'OK'})

def data_delete(request):
    "数据库删除记录"
    names = request.POST
    for idx in names:
        # 删除操作： PointSourceData包涵PointSouce外键，只要删除pointsource则父表中记录自动被删除
        PointSourceData.objects.get(station__stationName=names[idx]).delete()
        # PointSource.objects.get(stationName=names[idx]).delete()
    return JsonResponse(names)
    # return JsonResponse(names)


def data_geojson(request):
    "读取/media/geojson/data.geojson, 并以json数据返回"
    dataPath = os.path.join(settings.BASE_DIR, 'media', 'geojson','data.geojson')
    with open(dataPath) as f:
        data = f.read()
        return HttpResponse(data, content_type='text/plain')
    return HttpResponse("Error: file not found[%s]"%dataPath, content_type='text/plain')
