# city.py : data process for City Model in <models.py>
# author: Edward Qiu <qkx2010@aliyun.com>
# created: 2017/11/29

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from ahhost.models import Province
import geojson
import os

def saveToORM(request):
    "读取</media/geojson/provinces/data.geojson>数据，导入到Province model数据库中"
    dataPath = os.path.join(settings.BASE_DIR, 'media', 'geojson','provinces', 'data.geojson')
    with open(dataPath) as f:
        data = f.read()
        decodedData = geojson.loads(data)

        for item in decodedData['features']:
            province = Province(
                ID=item['properties']['ADMINCODE'],
                name=item['properties']['NAME'],
                minx=item['properties']['minx'],
                miny=item['properties']['miny'],
                maxx=item['properties']['maxx'],
                maxy=item['properties']['maxy']
                )
            province.save()
    return JsonResponse({'status': 'OK'})

def getAll(request):
    data = {}
    qs = Province.objects.values()
    for idx,item in enumerate(qs):
        data[idx] = item
    return JsonResponse(data)
