import requests, bs4, os, json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from ahhost.models import PointSource, PointSourceData
from ahhost.DataHandler import DataHandler
import datetime as dt
from django_pandas.io import read_frame
from ahhost.Gridding import ShapeFileHandler,NCHandler,RasterHandler


def index(request):
    return render(request,'index.html')


def data_import(request):
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
    df = dh.loadExcel('media/安徽省排放清单估算结果-2015.11.xlsx')
    df2 = df.ix[:, :19]
    df2.columns = COL
    dh.saveToORM(df2, dt.date(2015, 11, 1))
    return HttpResponse('ok')

def data_load(request):
    "从数据库中提取污染源监测数据"
    data = []
    qs = PointSourceData.objects.all()
    for record in qs:
        data.append([
            record.station.stationName,
            record.station.areaId,
            record.station.industryName,
            "%.1f" %record.SO2,
            "%.1f" %record.NOX,
            "%.1f" %record.CO,
            "%.1f" %record.PM,
            "%.1f" %record.PM10,
            "%.1f" %record.PM25,
            "%.1f" %record.NMVOC,
            "%.1f" %record.NH3,
            ])
    # df = read_frame(qs)
    # data = df[['station','SO2','NOX','CO','PM','PM10','PM25','NMVOC','NH3']]

    return JsonResponse({'data': data})
    # return JsonResponse({'data': df.to_json(orient='records')})

def shapefile_create(request):
    "get ajax POST request and create shapefile with custom parameters"
    parameters = request.POST
    latlon = [float(parameters['miny']), float(parameters['minx']),\
        float(parameters['maxy']), float(parameters['maxx'])]
    sfh = ShapeFileHandler(latlon,
        float(parameters['resolution']))
    filepath = os.path.join('media/shapefiles/grid')
    sfh.export(filepath)

    return JsonResponse({'status': 'OK', 'filename': filepath})


def raster_calculate(request):
    "calculte raster grid based on zonal_stats, then output netCDF4 file"
    parameters = request.POST
    # step 1:zonal_stats and data normalized
    rasterURL = 'media/{0}/{1}/2010.tif'.format(parameters['st'],parameters['Area'])
    vectorURL = 'media/shapefiles/grid.shp'
    rh = RasterHandler(rasterURL, vectorURL)
    rh.process()
    rawGeojson = rh.normalized()
    # step 2:export geojson file to 'media/geojson/data.geojson'
    rh.export_geojson('media/geojson/data.geojson')
    # step 3:netCDF4 file export
    nh = NCHandler(rawGeojson, 'media/netcdf4/data.nc')
    resolution = float(parameters['resolution'])/100.0
    pollution = {
        'name': parameters['type'],
        'quantity': float(parameters['sum'])
    }
    nh.process(parameters['Area'], pollution, resolution)

    return JsonResponse({'status': 'OK'})
