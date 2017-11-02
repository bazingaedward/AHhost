# Plot contour for Temperature ,wind.... in ShiJiaZhuang
# author: qkx <bazingaedward@gmail.com>
# created: 2017/08/30

# let tkinker not using display x-window
import matplotlib
matplotlib.use('Agg')

import os
import tempfile
import numpy as np
import json
from mpl_toolkits.basemap import Basemap
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
import shapefile as sf
from matplotlib.mlab import griddata
from shapely.geometry import Polygon as ShapelyPolygon
from shapely.geometry import Point as ShapelyPoint


PLOTLATLON = [113.4, 115.8, 37.3, 38.9]
SJZ_Center = [38.03, 114.48]
PLOT_Interval = 100
SJZ_Shape_Path = '/chinkun/data/raw/gis/shp/shi'

def plotTest():
    jsonPath = '../../data/data_per5min/2017/09/14/merged_data_noQ_GMT-8_20170914092000.json'
    xi, yi,zi = Preprocessing(jsonPath=jsonPath, var='WIN_S_Avg_1mi')
    plotWind(xi, yi, zi, save_dir='./')

def Preprocessing(jsonPath, var='TEM', missing='999999'):
    """
        功能：
            json实时数据预处理
        输入：
            jsonPath:实时json数据相对路径
            var:绘制的变量名，默认为温度‘TEM’
            missing：数据缺测值，默认’999999’
        输出：
            xi: 插值格点后的经向numpy array
            yi: 插值格点后的纬向numpy array
            zi: 经过matplotlib.mlab.griddata插值后的二维numpy array
    """
    with open(jsonPath) as data_file:
        data = json.load(data_file)
        x = []
        y = []
        varList = []
        for station in data:
            if not var in station or station[var] == missing:
                # Temperature.append(np.NaN)
                pass
            else:
                varList.append(float(station[var]))
                x.append(float(station['Lon']))
                y.append(float(station['Lat']))

        # define grid.
        xi = np.linspace(PLOTLATLON[0], PLOTLATLON[1], PLOT_Interval)
        yi = np.linspace(PLOTLATLON[2], PLOTLATLON[3], PLOT_Interval)
        # grid the data.
        zi = griddata(np.array(x), np.array(y), np.array(varList), xi, yi, interp='linear')
        return xi, yi, zi


def plotTempature(xi, yi, zi, save_dir='.'):
    """
        功能：
            绘制温度等值线
        输入：
            xi: 插值格点后的经向numpy array
            yi: 插值格点后的纬向numpy array
            zi: 经过matplotlib.mlab.griddata插值后的二维numpy array
        输出：
            save_dir/tempfile.png
    """
    fig = plt.figure(frameon=False)
    ax = fig.add_subplot(111)

    map = Basemap(llcrnrlon=PLOTLATLON[0],llcrnrlat=PLOTLATLON[2],\
                 urcrnrlon=PLOTLATLON[1],urcrnrlat=PLOTLATLON[3],\
                 resolution='i', projection='merc', lat_0 = SJZ_Center[0], lon_0 = SJZ_Center[1])

    # map.readshapefile(SJZ_Shape_Path, 'sjz')
    # 调整格点投影坐标
    x1, y1 = map(xi, yi)
    # 网格化经纬度网格
    xx, yy = np.meshgrid(x1, y1)
    # print(zi.shape)
    # 绘图等值线
    PCM = map.pcolor(xx, yy, zi, alpha=1, cmap='coolwarm')
    # CS = map.contour(xx, yy, zi,\
    #             alpha=0.8,
    #             linestyles = 'dashed',
    #             levels = np.arange(np.min(zi),np.max(zi),1)
    #             )
    # CS_label = plt.clabel(CS, inline=True, inline_space=10, fontsize=8, fmt='%2.0f', colors='k')
    # print(CS.collections)
    # 裁剪边缘
    sjz = sf.Reader(SJZ_Shape_Path)
    for shape_rec in sjz.shapeRecords():
        # print(shape_rec.record)
        vertices = []
        codes = []
        pts = shape_rec.shape.points
        prt = list(shape_rec.shape.parts) + [len(pts)]
        for i in range(len(prt) - 1):
            for j in range(prt[i], prt[i+1]):
                vertices.append(map(pts[j][0], pts[j][1]))
            codes += [Path.MOVETO]
            codes += [Path.LINETO] * (prt[i+1] - prt[i] -2)
            codes += [Path.CLOSEPOLY]
        clip = Path(vertices, codes)
        clip = PathPatch(clip, transform=ax.transData)

    # for contour in CS.collections:
        # contour.set_clip_path(clip)

    clip_map_shapely = ShapelyPolygon(vertices)

    # for text_object in CS_label:
    #     if not clip_map_shapely.contains(ShapelyPoint(text_object.get_position())):
    #         text_object.set_visible(False)

    PCM.set_clip_path(clip)
    plt.axis('off')

    # 保存结果图片
    filePath = tempfile.mktemp(suffix='.png', prefix='tmp_', dir=save_dir)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    plt.savefig(filePath, bbox_inches='tight', pad_inches=0, transparent=True, dpi=200)
    return filePath

def plotHumidity(xi, yi, zi, save_dir='.'):
    """
        功能：
            绘制湿度等值线
        输入：
            xi: 插值格点后的经向numpy array
            yi: 插值格点后的纬向numpy array
            zi: 经过matplotlib.mlab.griddata插值后的二维numpy array
        输出：
            save_dir/tempfile.png
    """
    fig = plt.figure(frameon=False)
    ax = fig.add_subplot(111)

    map = Basemap(llcrnrlon=PLOTLATLON[0],llcrnrlat=PLOTLATLON[2],\
                 urcrnrlon=PLOTLATLON[1],urcrnrlat=PLOTLATLON[3],\
                 resolution='i', projection='merc', lat_0 = SJZ_Center[0], lon_0 = SJZ_Center[1])

    # map.readshapefile(SJZ_Shape_Path, 'sjz')
    # 调整格点投影坐标
    x1, y1 = map(xi, yi)
    # 网格化经纬度网格
    xx, yy = np.meshgrid(x1, y1)
    # print(zi.shape)
    # 绘图等值线
    PCM = map.pcolor(xx, yy, zi, alpha=1, cmap='Blues')
    # CS = map.contour(xx, yy, zi,\
    #             alpha=0.8,
    #             linestyles = 'dashed',
    #             levels = np.arange(0,100,5)
    #             )
    # CS_label = plt.clabel(CS, inline=True, inline_space=10, fontsize=8, fmt='%2.0f', colors='k')
    # print(CS.collections)
    # 裁剪边缘
    sjz = sf.Reader(SJZ_Shape_Path)
    for shape_rec in sjz.shapeRecords():
        # print(shape_rec.record)
        vertices = []
        codes = []
        pts = shape_rec.shape.points
        prt = list(shape_rec.shape.parts) + [len(pts)]
        for i in range(len(prt) - 1):
            for j in range(prt[i], prt[i+1]):
                vertices.append(map(pts[j][0], pts[j][1]))
            codes += [Path.MOVETO]
            codes += [Path.LINETO] * (prt[i+1] - prt[i] -2)
            codes += [Path.CLOSEPOLY]
        clip = Path(vertices, codes)
        clip = PathPatch(clip, transform=ax.transData)

    # for contour in CS.collections:
    #     contour.set_clip_path(clip)

    clip_map_shapely = ShapelyPolygon(vertices)

    # for text_object in CS_label:
    #     if not clip_map_shapely.contains(ShapelyPoint(text_object.get_position())):
    #         text_object.set_visible(False)

    PCM.set_clip_path(clip)
    plt.axis('off')

    # 保存结果图片
    filePath = tempfile.mktemp(suffix='.png', prefix='tmp_', dir=save_dir)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    plt.savefig(filePath, bbox_inches='tight', pad_inches=0, transparent=True, dpi=200)

    return filePath

def plotPrecipitation(xi, yi, zi, save_dir='.'):
    """
        功能：
            绘制降水等值线
        输入：
            xi: 插值格点后的经向numpy array
            yi: 插值格点后的纬向numpy array
            zi: 经过matplotlib.mlab.griddata插值后的二维numpy array
        输出：
            save_dir/tempfile.png
    """
    # 检验是否数值全为0
    if not np.count_nonzero(zi):
        return ''
    fig = plt.figure(frameon=False)
    ax = fig.add_subplot(111)

    map = Basemap(llcrnrlon=PLOTLATLON[0],llcrnrlat=PLOTLATLON[2],\
                 urcrnrlon=PLOTLATLON[1],urcrnrlat=PLOTLATLON[3],\
                 resolution='i', projection='merc', lat_0 = SJZ_Center[0], lon_0 = SJZ_Center[1])

    # map.readshapefile(SJZ_Shape_Path, 'sjz')
    # 调整格点投影坐标
    x1, y1 = map(xi, yi)
    # 网格化经纬度网格
    xx, yy = np.meshgrid(x1, y1)
    # print(zi.shape)
    # 绘图等值线
    PCM = map.pcolor(xx, yy, zi, alpha=1, cmap='Blues')
    # CS = map.contour(xx, yy, zi,\
    #             alpha=0.8,
    #             linestyles = 'dashed',
    #             levels = np.arange(np.min(zi),np.max(zi),20)
    #             )
    # CS_label = plt.clabel(CS, inline=True, inline_space=10, fontsize=8, fmt='%2.0f', colors='k')
    # print(CS.collections)
    # 裁剪边缘
    sjz = sf.Reader(SJZ_Shape_Path)
    for shape_rec in sjz.shapeRecords():
        # print(shape_rec.record)
        vertices = []
        codes = []
        pts = shape_rec.shape.points
        prt = list(shape_rec.shape.parts) + [len(pts)]
        for i in range(len(prt) - 1):
            for j in range(prt[i], prt[i+1]):
                vertices.append(map(pts[j][0], pts[j][1]))
            codes += [Path.MOVETO]
            codes += [Path.LINETO] * (prt[i+1] - prt[i] -2)
            codes += [Path.CLOSEPOLY]
        clip = Path(vertices, codes)
        clip = PathPatch(clip, transform=ax.transData)

    # for contour in CS.collections:
    #     contour.set_clip_path(clip)

    clip_map_shapely = ShapelyPolygon(vertices)

    # for text_object in CS_label:
    #     if not clip_map_shapely.contains(ShapelyPoint(text_object.get_position())):
    #         text_object.set_visible(False)

    PCM.set_clip_path(clip)
    plt.axis('off')

    # 保存结果图片
    filePath = tempfile.mktemp(suffix='.png', prefix='tmp_', dir=save_dir)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    plt.savefig(filePath, bbox_inches='tight', pad_inches=0, transparent=True, dpi=200)

    return filePath

def plotVisibility(xi, yi, zi, save_dir='.'):
    """
        功能：
            绘制能见度等值线
        输入：
            xi: 插值格点后的经向numpy array
            yi: 插值格点后的纬向numpy array
            zi: 经过matplotlib.mlab.griddata插值后的二维numpy array
        输出：
            save_dir/tempfile.png
    """
    fig = plt.figure(frameon=False)
    ax = fig.add_subplot(111)

    map = Basemap(llcrnrlon=PLOTLATLON[0],llcrnrlat=PLOTLATLON[2],\
                 urcrnrlon=PLOTLATLON[1],urcrnrlat=PLOTLATLON[3],\
                 resolution='i', projection='merc', lat_0 = SJZ_Center[0], lon_0 = SJZ_Center[1])

    # map.readshapefile(SJZ_Shape_Path, 'sjz')
    # 调整格点投影坐标
    x1, y1 = map(xi, yi)
    # 网格化经纬度网格
    xx, yy = np.meshgrid(x1, y1)
    # print(zi.shape)
    # 绘图等值线
    zi /= 1000 # meter to kilometer
    PCM = map.pcolor(xx, yy, zi, alpha=1, cmap='coolwarm')
    # CS = map.contour(xx, yy, zi,\
    #             alpha=0.8,
    #             linestyles = 'dashed',
    #             levels = np.arange(np.min(zi),np.max(zi),3)
    #             )
    # CS_label = plt.clabel(CS, inline=True, inline_space=10, fontsize=7, fmt='%2.0f', colors='w')
    # print(CS.collections)
    # 裁剪边缘
    sjz = sf.Reader(SJZ_Shape_Path)
    for shape_rec in sjz.shapeRecords():
        # print(shape_rec.record)
        vertices = []
        codes = []
        pts = shape_rec.shape.points
        prt = list(shape_rec.shape.parts) + [len(pts)]
        for i in range(len(prt) - 1):
            for j in range(prt[i], prt[i+1]):
                vertices.append(map(pts[j][0], pts[j][1]))
            codes += [Path.MOVETO]
            codes += [Path.LINETO] * (prt[i+1] - prt[i] -2)
            codes += [Path.CLOSEPOLY]
        clip = Path(vertices, codes)
        clip = PathPatch(clip, transform=ax.transData)

    # for contour in CS.collections:
    #     contour.set_clip_path(clip)

    clip_map_shapely = ShapelyPolygon(vertices)

    # for text_object in CS_label:
    #     if not clip_map_shapely.contains(ShapelyPoint(text_object.get_position())):
    #         text_object.set_visible(False)

    PCM.set_clip_path(clip)
    plt.axis('off')

    # 保存结果图片
    filePath = tempfile.mktemp(suffix='.png', prefix='tmp_', dir=save_dir)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    plt.savefig(filePath, bbox_inches='tight', pad_inches=0, transparent=True, dpi=200)

    return filePath

def plotWind(xi, yi, zi, save_dir='.'):
    """
        功能：
            绘制风场等值线
        输入：
            xi: 插值格点后的经向numpy array
            yi: 插值格点后的纬向numpy array
            zi: 经过matplotlib.mlab.griddata插值后的二维numpy array
        输出：
            save_dir/tempfile.png
    """
    fig = plt.figure(frameon=False)
    ax = fig.add_subplot(111)

    map = Basemap(llcrnrlon=PLOTLATLON[0],llcrnrlat=PLOTLATLON[2],\
                 urcrnrlon=PLOTLATLON[1],urcrnrlat=PLOTLATLON[3],\
                 resolution='i', projection='merc', lat_0 = SJZ_Center[0], lon_0 = SJZ_Center[1])

    # map.readshapefile(SJZ_Shape_Path, 'sjz')
    # 调整格点投影坐标
    x1, y1 = map(xi, yi)
    # 网格化经纬度网格
    xx, yy = np.meshgrid(x1, y1)
    # print(zi.shape)
    # 绘图等值线
    PCM = map.pcolor(xx, yy, zi, alpha=1, cmap='coolwarm')
    # CS = map.contour(xx, yy, zi,\
    #             alpha=0.8,
    #             linestyles = 'dashed',
    #             levels = np.arange(np.min(zi),np.max(zi),0.5)
    #             )
    # CS_label = plt.clabel(CS, inline=True, inline_space=10, fontsize=8, fmt='%2.1f', colors='k')
    # print(CS.collections)
    # 裁剪边缘
    sjz = sf.Reader(SJZ_Shape_Path)
    for shape_rec in sjz.shapeRecords():
        # print(shape_rec.record)
        vertices = []
        codes = []
        pts = shape_rec.shape.points
        prt = list(shape_rec.shape.parts) + [len(pts)]
        for i in range(len(prt) - 1):
            for j in range(prt[i], prt[i+1]):
                vertices.append(map(pts[j][0], pts[j][1]))
            codes += [Path.MOVETO]
            codes += [Path.LINETO] * (prt[i+1] - prt[i] -2)
            codes += [Path.CLOSEPOLY]
        clip = Path(vertices, codes)
        clip = PathPatch(clip, transform=ax.transData)

    # for contour in CS.collections:
    #     contour.set_clip_path(clip)

    clip_map_shapely = ShapelyPolygon(vertices)

    # for text_object in CS_label:
    #     if not clip_map_shapely.contains(ShapelyPoint(text_object.get_position())):
    #         text_object.set_visible(False)

    PCM.set_clip_path(clip)
    plt.axis('off')

    # 保存结果图片
    filePath = tempfile.mktemp(suffix='.png', prefix='tmp_', dir=save_dir)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    plt.savefig(filePath, bbox_inches='tight', pad_inches=0, transparent=True, dpi=200)

    return filePath

if __name__ == '__main__':
    plotTest()
