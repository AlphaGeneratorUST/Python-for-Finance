import tushare as ts
import datetime as dt
import sys
sys.path.append('..')
from database.mongo import ResultDBs
from database.mongodb import mongodb
import pandas as pd
import traceback
import math
from help.date import get_quarters


class database(object):
    '''
    存储数据
    '''
    def __init__(self, data=None, indexList=None, tableName=None, save=False):
        self.data = data
        self.indexList = indexList
        self.tableName = tableName
        if save:
            self.save()

    def save(self):
        if self.data is not None:
            data = self.data.to_dict('records')
            indexList = self.indexList
            tableName = self.tableName
            db = ResultDBs(tableName, indexList)
            db.save(data)


class SymbolMdm(object):
    """
    股票基础数据，存储到dataframe中
    """
    def __init__(self, save=True):
        """
        code,代码
        name，名称
        industry，所属行业
        area，地区
        pe,市盈率
        outstanding，流通股本（亿）
        gpr, 毛利率（%）
        npr, 净利润率（%）
        :param save:
        """
        try:
            stockBasics = ts.get_stock_basics()
        except:
            stockBasics = None

        if stockBasics is not None:
            now = dt.datetime.now()
            stockBasics['datatime'] = now.strftime('%Y-%m-%d')
            stockBasics['datatimestramp'] = now.strftime('%H:%M:%S')
            stockBasics['code'] = stockBasics.index
            indexlist = ['code','datatime'] ##数据库索引
            tableName = 'SymbolMdm'
            print(self.__name__)
            database(stockBasics,indexlist,tableName,save)


class companyReport(object):
    """
    公司业绩报告
    """
    def __init__(self, year=None, quarter=None, save=True, updateAll=False, beginyear=1990, beginquarter=1):
        """
        获取季度的公司业绩报告
        :param year: 年份
        :param quarter: 季度
        :param save:
        :param updateAll:
        :param beginyear:
        :param beginquarter:
        """
        now = dt.datetime.now()
        if year is None or quarter is None:
            year = now.year
            quarter = math.ceil(now.month/3.0)

        if not updateAll:
            try:
                profitData = ts.get_report_data(year,quarter)
                profitData['datatime'] = now.strftime('%Y-%M-%d')
                profitData['datatimestramp'] = now.strftime('%H:%M:%S')
                profitData['year'] = year
                profitData['quarter'] = quarter
                indexlist = ['code','year','quarter']
                tableName = 'companyReport'
                database(profitData,indexlist,tableName,save)
            except:
                traceback.print_exc()
        else:
            ## 生成季度时间序列
            quarters = get_quarters((beginyear,beginquarter),(year,quarter))
            for y,q in quarters:
                companyRepor(y,q) ## 递归获取所有历史数据


class HistData(object):
    '''
    获取股票历史数据
    '''
    def __init__(self,code=None,start=None,end=None,save=True):
        """
        get symbol historical data
        :param code:
        :param start:
        :param end:
        :param save:
        """
        now = dt.datetime.now()
        if end is None:
            end = (now - dt.timedelta(1)).strftime('%Y-%m-%d')
        if start is None:
            start = '1990-01-01'

        if code is None:
            mongo = mongodb() ## 获取股票代码
            collectname = 'SymbolMdm'
            where = {}
            kwargs = {'code':1}
            codes = mongo.select(collectname,where,kwargs)
            for code in codes:
                HistData(code.get('code'),HistData,end)
        else:
            try:
                data = ts.get_hist_data(code,start=start,end=end)
                data['datatime'] = now.strftime('%Y-%m-%d')
                data['datatimestramp'] = now.strftime('%H:%M:%S')
                data['date'] = data.index
                data['code'] = code
                indexlist = ['code', 'date']
                tableName = 'HistData'
                database(data,indexlist,tableName,save)
                print('info:{} downloaded is ok, num:{}'.format(code,len(data)))
            except:
                pass


class symbClassfied(object):
    '''
    行业分类
    概念分类
    地域分类
    中小板分类
    创业板分类
    风险警示板分类
    沪深300成分股及权重
    上证50成分股
    中证500成分股
    终止上市股票列表
    暂停上市股票列表
    '''
    def __init__(self,save=True):
        '''
        :param save:
        '''
        self.columns = ['code',
                        'name',
                        'comceptName',
                        'areaName',
                        'smeName',
                        'gemName',
                        'stName',
                        'hs300s',
                        'sz50s',
                        'zz500s',
                        'terminated',
                        'suspended']
        self.data = None
        self.get_industry_classified()
        self.get_concept_classified()
        self.get_area_classified()
        self.get_sme_classified()
        self.get_gem_classified()
        self.get_st_classified()
        self.get_hs300s_classified()
        self.get_sz50s_classified()
        self.get_zz500s_classified()
        self.get_terminated_classified()
        self.get_suspended_classified()
        now = dt.datetime.now()
        self.data['datatime'] = now.strftime('%Y-%m-%d')
        self.data['datatimestramp'] = now.strftime('%H:%M:%S')
        indexlist = ['code', 'datatime']
        tableName = 'symbClassified'
        database(self.data, indexlist, tableName, save)

    def get_industry_classified(self):
        '''
        行业分类
        :return:
        '''
        pass

    def get_concept_classified(self):
        """
        概念分类
        :return:
        """
        pass





