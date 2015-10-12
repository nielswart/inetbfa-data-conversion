﻿# Copyright 2015 Intersect Technologies CC
# 
'''
Created on Sat May 23 15:22:03 2015
@author: Niel Swart
'''

import numpy as np
import pandas as pd
from datamanager.load import get_equities
from quantstrategies.universe_selection import liquid_jse_shares
from quantstrategies.filters import apply_filter

def fields():
    return [
        'Close',
        'Market Cap',
        'Volume',
        'Total Number Of Shares',
        'VWAP'
    ]

def filter(data):
    '''
    Uses the Market Cap, Volume, Close, Total Number Of Shares to filter shares
    '''
    assert isinstance(data, dict)

    return(apply_filter(liquid_jse_shares, data))

def transform(data):
    '''
    Calculate the momentum
    '''
    assert isinstance(data, dict)

    fc = data['Close'].sort(ascending=False)
    mom12 = np.log(fc.shift(-21)) - np.log(fc.shift(-252))

    out = {}
    out = data.copy()
    out['Momentum - 12M'] = mom12
    return out

def security_selection(data):
    '''
    Select the top 15 securities based on momentum
    '''
    assert isinstance(data, dict)

    latest_mom = data['Momentum - 12M'].ix[0]
    cols = [
        'fullname',
        'industry',
        'sector'
    ]

    equities = get_equities()
    output = equities[cols].ix[data['Close'].columns].copy()

    output['Momentum - 12M'] = latest_mom
    output['Price'] = data['Close'].last('1D').ix[0]
    return(output.sort(columns = 'Momentum - 12M', ascending = False))

def portfolio_selection(data):
    '''
    '''

    assert isinstance(data, pd.DataFrame)
    return(data.ix[:15])


