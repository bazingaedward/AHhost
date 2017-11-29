# city.py : data process for Province Model in <models.py>
# author: Edward Qiu <qkx2010@aliyun.com>
# created: 2017/11/28

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from ahhost.models import Province
import geojson
import os

def saveToORM(request):
    "读取</media/geojson/AH_cities.geojson>数据，导入到City model数据库中"
    dataPath = os.path.join(settings.BASE_DIR, 'media', 'geojson','AH_cities.geojson')
    with open(dataPath) as f:
        data = f.read()
        return HttpResponse(data, content_type='text/plain')
    return HttpResponse("Error: file not found[%s]"%dataPath, content_type='text/plain')
