import requests, bs4, os, json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.conf import settings
from ahhost.models import PointSource, PointSourceData
from ahhost.DataHandler import DataHandler
import datetime as dt
from django_pandas.io import read_frame
from ahhost.Gridding import ShapeFileHandler,NCHandler,RasterHandler


def index(request):
    return render(request,'index.html')


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
        PointSourceData.objects.get(station__stationName=names[idx]).delete()
    return JsonResponse({'status': 'OK'})

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


def upload_file(request):
    # parameters = request.POST
    def handle_uploaded_file(f):
        # save files
        with open('media/excel/data.xlsx', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        # data import
        data_import(request, request.POST.get('dt'))

    if request.method == 'POST':
        handle_uploaded_file(request.FILES['exfile'])
        # return JsonResponse(parameters)
        return HttpResponseRedirect('/')
    # else:
    #     form = UploadFileForm()
    # return render(request, 'upload.html', {'form': form})
    # return HttpResponseRedirect('/')
