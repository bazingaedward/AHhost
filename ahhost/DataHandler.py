# DataHandler.py : provide DataHandler class for pollution source data import/outport
# author: Edward Qiu <qkx2010@aliyun.com>
# created: 2017/09/26

import os
import pandas
import datetime as dt

from ahhost.models import PointSource,PointSourceData
from django.conf import settings
from sqlalchemy import create_engine

class DataHandler:
    def __init__(self):
        database_name = settings.DATABASES['default']['NAME']
        database_url = 'sqlite:///project.db'
        # database_url = 'sqlite:///{database_name}'.format(database_name=database_name)
        self.engine = create_engine(database_url, echo=False)

    def loadExcel(self, path, sheetname=0):
        df = pandas.read_excel(path, sheetname)
        return df

    def saveToTable(self, df, sqlTable, exist_action='append'):
        df.to_sql(sqlTable, self.engine, if_exists=exist_action)

    def saveToORM(self, df, date):
        "save pandas dataframe to Django ORM"
        for idx,row in df.iterrows():
            if not PointSource.objects.filter(stationName=row['stationName']):
                station = PointSource(
                    stationName = row['stationName'],
                    areaId = row['areaId'],
                    province = row['province'],
                    city = row['city'],
                    county = row['county'],
                    street = row['street'],
                    address = row['address'],
                    longitude = row['longitude'],
                    latitude = row['latitude'],
                    industryId = row['industryId'],
                    industryName = row['industryName'],
                )
                station.save()
            else:
                station = PointSource.objects.get(stationName=row['stationName'])
            data = PointSourceData(
                station = station,
                SO2 = row['SO2'],
                NOX = row['NOX'],
                CO = row['CO'],
                PM = row['PM'],
                PM10 = row['PM10'],
                PM25 = row['PM25'],
                NMVOC = row['NMVOC'],
                NH3 = row['NH3'],
                date = date
            )
            data.save()

    def queryDB(self, sql_sentence):
        conn = self.engine.connect()
        result = conn.execute(sql_sentence)
        for row in result:
            print(row)
        conn.close()
        return result
