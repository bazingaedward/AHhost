# Interpolation.py : provide GIS interpolation for Pollutions
# author: Edward Qiu <qkx2010@aliyun.com>
# created: 2017/11/30

import os
import numpy as np
import math
import netCDF4 as nc
from ahhost.models import Province
from scipy.interpolate import griddata

class PointSourceInterpolation:
    """
        PointSourceInterpolation: 基于用户输入信息生成经纬度网格的shape文件
        输入：
            latlon：[lat_min,lon_min,lat_max,lon_max]
            resolution: 1
        输出：
            NetCDF4 File
    """
    def __init__(self, latlon, resolution=1):
        self.latlon = latlon
        self.resolution = resolution
        self.w = sf.Writer(shapeType=sf.POLYGON)
        self.w.autoBalance = 1
