# -*- coding: utf-8 -*-
"""
Created on Sun May 17 14:55:49 2015

@author: Niel
"""

from os import path, listdir, makedirs
import pandas as pd
import numpy as np

import datetime as dt
import datamanager.datamodel as dm
from datamanager.datamodel import MarketData
from datamanager.envs import *
from quantstrategies.filters import greater_than_filter, less_than_filter, top_filter
from quantstrategies.date_utils import last_month_end, date_days_ago

def calc_means(data, fields, period = '1M'):
    
    means = {}
    for f in fields:
        data[f].fillna(method = 'pad', inplace=True)
        means[f] = data[f].last(period).mean()
        
        if type(means[f]) != pd.Series:
            raise TypeError
        
    return means

class Momentum(object):
    """
    """

    def __init__(self, start_date, end_date):
        '''
        '''
        self.start_date = '2014-06-01'
        self.end_date = '2015-05-31'
        
        daily_path = path.join(DATA_PATH, 'jse', 'equities', 'daily')
        fields = [
            'Close',
            'Market Cap',
            'Volume',
            'Total Number Of Shares',
            'DY',
            'PE',
            'VWAP'
        ]
        # Import the last 12 month's data
        self.data = MarketData.load_from_file(daily_path, fields, start_date, end_date)

        self.means = calc_means(self.data, fields)

    def filter_universe(self, listed):
        '''
        Apply filters
        '''

        filtered = listed

        # Volume zero filter
        filtered = filtered.intersection(greater_than_filter(self.means['Volume'], 1))

        # Price filter
        filtered = filtered.intersection(greater_than_filter(self.data['Close'].last('1D').ix[0], 100))
    
        # Market Cap filter
        filtered = filtered.intersection(top_filter(self.means['Market Cap'], 200))
    
        # Trading Frequency Filter
        filtered = filtered.intersection(greater_than_filter((self.means['Volume']/self.means['Total Number Of Shares'])*100, 0.01))
    
        return(filtered)

    def calc_momentum(self):
        '''
        Calculate momentum
        '''
        # Select Universe
        listed = dm.get_all_listed()
        filtered = self.filter_universe(listed)
        fc = self.data['Close'][filtered].sort(ascending=False)

        last_close = fc.ix[self.end_date] # should be Series
        mom12 = np.log(fc.shift(-21)) - np.log(fc.shift(-252))
        mom6 = np.log(fc) - np.log(fc.shift(-126))
        mom3 = np.log(fc) - np.log(fc.shift(-63))
   
        # TODO: get intersection of top 100 of all momentum

        # TODO: calculate linearity of momentum

        # TODO: filter on linearity

        # TODO: calculate minimum variance portfolio of resulting stocks


        equities = dm.get_equities()

        cols = [
        'fullname',
        'industry',
        'sector'
        ]

        output = equities[cols].ix[filtered].copy()

        output['Momentum - 12M'] = mom12.last('1D').ix[0]
        output['Momentum - 6M'] = mom6.last('1D').ix[0]
        output['Momentum - 3M'] = mom3.last('1D').ix[0]
        output['Price'] = self.data['Close'].last('1D').ix[0]
        output['DY'] = self.data['DY'][filtered].last('1D').ix[0]
        output['PE'] = self.data['PE'][filtered].last('1D').ix[0]

        # RANK
        return(output.sort(columns = 'Momentum - 6M', ascending = False))

    def save(self):

        # C:\root\OneDrive\Intersect Technologies\Intersect Invest\Products
        self.calc_momentum().to_excel(path.join('C:\\', 'root', 'OneDrive', 'Intersect Technologies', 'Intersect Invest', 'Products', 'Portfolios', 'Growth Portfolio - ' + str(dt.date.today()) + '.xlsx'))