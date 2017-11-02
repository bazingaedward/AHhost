import requests, bs4, os, json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from . import plot as pl


def realtime(request):
    return render(request, 'weather/realtime.html', {
        'DEBUG': settings.DEBUG,
    })


def realtime_latest(request):
    content = ''
    filename = os.path.join(settings.DATA_ROOT, 'data_per5min', 'latest.json')
    with open(filename) as f:
        content = f.read()

    return HttpResponse(content, content_type='application/json')


def realtime_data(request, param):
    content = ''
    filename = os.path.join(settings.DATA_ROOT, param)
    with open(filename) as f:
        content = f.read()

    return HttpResponse(content, content_type='application/json')


def radar(request):
    url = 'http://products.weather.com.cn/product/radar/index/procode/JC_RADAR_AZ9311_JB'

    html = '<b>暂时不能获取雷达数据！</b>'

    try:
        r = requests.get(url)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')

        soup.find_all('div', class_='weather_li')[0]['style'] = 'display:none'
        soup.find_all('div', class_='weather_li_head')[0]['style'] = 'display:none'
        soup.find_all('div', class_='footer')[0]['style'] = 'display:none'
        soup.find_all('div', class_='tqyb_left')[0]['style'] = 'display:none'
        soup.find_all('div', class_='lddzcz')[0]['style'] = 'display:none'
        soup.find_all('div', class_='title')[0]['style'] = 'display:none'
        soup.find_all('ul', class_='weather')[0]['style'] = 'display:none'

        html = soup.prettify()
    except:
        pass

    return render(request, 'weather/radar.html', {
        'html': html
    })

def plot(request):
    data = request.GET
    jsonPath = os.path.join('../data/data_per5min', data['date'], data['filename'])
    # jsonPath = '../data/data_per5min/2017/07/29/merged_data_GMT-8_20170729165000.json'
    xi, yi,zi = pl.Preprocessing(jsonPath=jsonPath, var=data['var'])
    # plot option
    if data['var'] == 'TEM':
        name = pl.plotTempature(xi, yi, zi, save_dir=data['save_dir'])
    elif data['var'] == 'RHU':
        name = pl.plotHumidity(xi, yi, zi, save_dir=data['save_dir'])
    elif data['var'] == 'PRE':
        name = pl.plotPrecipitation(xi, yi, zi, save_dir=data['save_dir'])
    elif data['var'] == 'VIS_HOR_1MI':
        name = pl.plotVisibility(xi, yi, zi, save_dir=data['save_dir'])
    else:
        name = pl.plotWind(xi, yi, zi, save_dir=data['save_dir'])

    content = {
        'imgName':name
    }

    return JsonResponse(content)

def test(request):
    return HttpResponse('hello world')
