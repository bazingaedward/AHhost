# Gridding.py : provide GIS grdding based on raster data of AnHui's population and GDP
# author: Edward Qiu <qkx2010@aliyun.com>
# created: 2017/10/21

import os
import shapefile as sf
import numpy as np
import math
from rasterstats import zonal_stats, point_query
from pprint import pprint
import netCDF4 as nc
import geojson

LATLONS = {
    'AH': [28.949517145902025,112.7214002962958,35.06114891777644,121.73919504342172]
}

class ShapeFileHandler:
    """
        ShapeFileHandler: 基于用户输入信息生成经纬度网格的shape文件
        输入：
            latlon：[lat_min,lon_min,lat_max,lon_max]
            resolution: 1
        输出：
            shapefile
    """
    def __init__(self, latlon, resolution=1):
        self.latlon = latlon
        self.resolution = resolution
        self.w = sf.Writer(shapeType=sf.POLYGON)
        self.w.autoBalance = 1

    def export(self, filename="grid"):
        "Calculate grid polygon and save to file"
        nx = int(math.ceil(abs(self.latlon[3] - self.latlon[1])/self.resolution))
        ny = int(math.ceil(abs(self.latlon[2] - self.latlon[0])/self.resolution))

        self.w.field("ID")
        id = 0
        for i in range(ny):
            for j in range(nx):
                id += 1
                vertices = []
                parts = []
                vertices.append([min(self.latlon[1] + self.resolution * j, self.latlon[3]),\
                    max(self.latlon[2] - self.resolution * i, self.latlon[0])])
                vertices.append([min(self.latlon[1] + self.resolution * (j+1), self.latlon[3]),\
                    max(self.latlon[2] - self.resolution * i, self.latlon[0])])
                vertices.append([min(self.latlon[1] + self.resolution * (j+1), self.latlon[3]),\
                    max(self.latlon[2] - self.resolution * (i+1), self.latlon[0])])
                vertices.append([min(self.latlon[1] + self.resolution * j, self.latlon[3]),\
                    max(self.latlon[2] - self.resolution * (i+1), self.latlon[0])])
                parts.append(vertices)
                self.w.poly(parts)
                self.w.record(id)

        self.w.save(filename)


class NCHandler:
    """
        NCHandler: rasterHandler的geojson数据导出成netCDF4文件
        输入：
            data: <geojson>
        输出：
            file：<netCDF4>
    """
    def __init__(self, data, output):
        self.rawdata = data
        self.rootgrp = nc.Dataset(output, "w", format="NETCDF4")

    def data_preprocess(self):
        "数据预处理：将geojson数据转换成二维数组"
        """ item example
            {'geometry': {'coordinates': [[(121.7214002962958, 29.061148917776443),
                                (121.73919504342172, 29.061148917776443),
                                (121.73919504342172, 28.949517145902025),
                                (121.7214002962958, 28.949517145902025),
                                (121.7214002962958, 29.061148917776443)]],
               'type': 'Polygon'},
              'id': '69',
              'properties': OrderedDict([('ID', '70'), ('sum', None)]),
              'type': 'Feature'}
        """
        data = []
        for item in self.rawdata:
            data.append(item['properties']['sum'])
        # pprint(data
        # replace list 'None' value with np.nan;reshape array with custom 2d array
        data = np.array(data, dtype=np.float).reshape((len(self.x),len(self.y)))
        return data/np.nansum(data)


    def process(self, area, pollution, resolution=0.1):
        latlon = LATLONS[area]
        self.y = np.arange(latlon[0], latlon[2], resolution)
        self.x = np.arange(latlon[1], latlon[3], resolution)
        # create dimensions
        lat = self.rootgrp.createDimension("lat", len(self.y))
        lon = self.rootgrp.createDimension("lon", len(self.x))

        # create variables and assignment
        latitudes = self.rootgrp.createVariable("lat","f4",("lat",))
        latitudes[:] = self.y[::-1]
        longitudes = self.rootgrp.createVariable("lon","f4",("lon",))
        longitudes[:] = self.x
        data = self.rootgrp.createVariable(pollution['name'],"f4",("lat","lon"))
        data[:] = self.data_preprocess() * pollution['quantity']
        self.rootgrp.close()


class RasterHandler:
    """
        RasterHandler: 网格化统计raster数据
        输入：
            raster：<file>
            vector: <file>
        输出：
            zonal_stats: <geojson>
    """
    def __init__(self, raster, vector):
        self.raster = raster
        self.vector = vector

    def process(self):
        # valid stats option= ['count', 'min', 'max', 'mean', 'sum', 'std', \
        #       'median', 'majority', 'minority', 'unique', 'range', 'nodata']
        self.stats = zonal_stats(self.vector, self.raster, stats=['sum'], geojson_out=True)
        #pprint(self.stats)
        return(self.stats)

    def normalized(self):
        "归一化数据"
        # sum
        total = 0.0
        maximum = 0.0
        for idx,item in enumerate(self.stats):
            data = item['properties']['sum']
            if data:
                total += float(data)
                if maximum < data:
                    maximum = data
            else:
                self.stats[idx]['properties']['sum'] = 0
        # normalizing
        for idx, item in enumerate(self.stats):
            data = item['properties']['sum']
            if data:
                self.stats[idx]['properties']['sum'] /= total
            self.stats[idx]['properties']['max'] = maximum / total

        return self.stats

    def export_geojson(self, filepath):
        "self.stats数据以geojson格式导出至文件"
        rawGeojson = {
            "type": "FeatureCollection",
            "features": self.stats
        }
        with open(filepath, 'w') as output:
            geojson.dump(rawGeojson, output)
