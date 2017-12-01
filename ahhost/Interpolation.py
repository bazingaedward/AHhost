# Interpolation.py : provide GIS interpolation for Pollutions
# author: Edward Qiu <qkx2010@aliyun.com>
# created: 2017/11/30

import os
import numpy as np
import pandas as pd
import netCDF4 as nc
from ahhost.models import Province, PointSourceData, PointSource
from scipy.interpolate import griddata
from pprint import pprint

class PointSourceInterpolation:
    """
        PointSourceInterpolation: 安徽省境内污染物点源数据的插值
        输入：
            variables: 需要插值的变量列表, eg: ['SO2'], 注意变量名为PointSOurceData
                        model 的字段定义名称
            method: 差值方法，包括['nearest','linear','cubic'], 默认'linear'
            resolution: 网格精度，默认0.5度
            storePath: 保存路径，eg:./test.nc
        输出：
            NetCDF4 File
    """
    def __init__(self):
        # get AH province data
        self.province = Province.objects.get(ID='340000')
        # get all PointSourceData,默认所有数据点都在安徽省境内
        self.data = pd.DataFrame(list(PointSourceData.objects.values()))
        # get all PointSource
        station = pd.DataFrame(list(PointSource.objects.values(
            'stationName', 'longitude', 'latitude')))
        station.columns = ['latitude', 'longitude', 'station_id']
        self.data = pd.merge(self.data, station, how='inner', on='station_id')
        # init results
        self.result = {}
        # print(self.data)

    def process(self, variables=[], method='linear', resolution=0.5):
        self.resolution = resolution
        grid_x, grid_y = np.mgrid[self.province.minx:self.province.maxx:resolution,
                                self.province.miny:self.province.maxy:resolution]
        self.shape = grid_x.shape
        for var in variables:
            self.result[var] = griddata(
                self.data[['longitude', 'latitude']].to_records(index=False).tolist(),
                self.data[var],
                (grid_x,grid_y),
                method=method
            )
        # print(self.result)

    def export(self, storePath='.'):
        self.rootgrp = nc.Dataset(os.path.join(storePath, 'Interpolate.nc'),
                                 "w", format="NETCDF4")
        # create dimensions
        lat = self.rootgrp.createDimension("lat", self.shape[1])
        lon = self.rootgrp.createDimension("lon", self.shape[0])
        # create variables
        lats = self.rootgrp.createVariable("lats","f4",("lat",))
        lats[:] = np.arange(self.province.miny, self.province.maxy, self.resolution)
        lons = self.rootgrp.createVariable("lons","f4",("lon",))
        lons[:] = np.arange(self.province.minx, self.province.maxx, self.resolution)
        for var in self.result.keys():
            data = self.rootgrp.createVariable(var,"f4",("lat","lon"))
            data[:] = self.result[var]
        # save and close file
        self.rootgrp.close()
