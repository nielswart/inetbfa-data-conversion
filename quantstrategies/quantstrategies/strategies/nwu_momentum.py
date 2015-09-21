﻿# Copyright 2015 Intersect Technologies CC
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
Created on Sat May 23 15:22:03 2015
@author: Niel Swart
'''

from os import path, listdir, makedirs
import pandas as pd
import numpy as np

import datetime as dt
import datamanager.datamodel as dm
from datamanager.datamodel import MarketData
from datamanager.load import get_equities
from datamanager.envs import *
from quantstrategies.strategies.model_portfolio import ModelPortfolio, calc_means
from quantstrategies.universe_selection import greater_than_filter, less_than_filter, top_filter, get_all_listed


class NWUMomentum(ModelPortfolio):
    """
    """

    def __init__(self, start_date, end_date):
        '''
        '''
        super(NWUMomentum, self).__init__(start_date, end_date)
        
        daily_path = path.join(DATA_PATH, 'jse', 'equities', 'daily')
        fields = [
            'Close',
            'Market Cap',
            'Volume',
            'Total Number Of Shares',
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

    def run(self):
        '''
        Calculate momentum
        '''
        # Select Universe
        listed = get_all_listed()
        # filter universe
        filtered = self.filter_universe(listed)
        fc = self.data['Close'][filtered].sort(ascending=False)

        mom12 = np.log(fc.shift(-21)) - np.log(fc.shift(-252))
        latest_mom = mom12.ix[0]
    
        equities = get_equities()

        cols = [
        'fullname',
        'industry',
        'sector'
        ]

        output = equities[cols].ix[filtered].copy()

        output['Momentum - 12M'] = latest_mom
        output['Price'] = self.data['Close'].last('1D').ix[0]
        # RANK
        return(output.sort(columns = 'Momentum - 12M', ascending = False))