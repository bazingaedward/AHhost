import os, json
import datetime as dt
from pprint import pprint
import pandas as pd
import geojson
from django.conf import settings
from django.shortcuts import render
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from ahhost.Gridding import ShapeFileHandler,NCHandler,RasterHandler
from ahhost.Interpolation import PointSourceInterpolation as PSI
def index(request):
    return render(request,'index.html')

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
    rasterURL = 'media/{0}/{1}/2010.tif'.format(parameters['st'],parameters['AreaID'])
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
    latlon = [
        float(parameters['miny']),
        float(parameters['minx']),
        float(parameters['maxy']),
        float(parameters['maxx']),
    ]
    nh.process(latlon, pollution, resolution)

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

def interpolate(request):
    parameters = request.POST
    psi = PSI()
    psi.process(
        variables=json.loads(parameters['var']),
        method=parameters['method'],
        resolution=float(parameters['resolution'])/100.0
        )
    psi.export(storePath=os.path.join(settings.MEDIA_ROOT,'netcdf4'))
    return JsonResponse({'status': 'OK'})
