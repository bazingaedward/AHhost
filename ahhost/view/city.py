# city.py : data process for City Model in <models.py>
# author: Edward Qiu <qkx2010@aliyun.com>
# created: 2017/11/28

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from ahhost.models import City
import geojson
import os

def saveToORM(request):
    "读取</media/geojson/AH_cities.geojson>数据，导入到City model数据库中"
    dataPath = os.path.join(settings.BASE_DIR, 'media', 'geojson','AH_Cities.geojson')
    with open(dataPath) as f:
        data = f.read()
        decodedData = geojson.loads(data)

        for item in decodedData['features']:
            city = City(
                ID=item['properties']['ADMINCODE'],
                name=item['properties']['name'],
                minx=item['properties']['minx'],
                miny=item['properties']['miny'],
                maxx=item['properties']['maxx'],
                maxy=item['properties']['maxy']
                )
            city.save()

    return JsonResponse({'status': 'OK'})
