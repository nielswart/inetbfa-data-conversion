﻿from datamanager.envs import *
from datamanager.adjust import *
import pandas as pd
import datetime as dt
import numpy as np
import random

def test_backwards_calc():
    '''
    '''

def test_adjusted_close():
    '''
    test should not be dependent on data in files
    '''
    
def test_book2market():
    '''
    '''
    
    dt_ix = [dt.date(2016, 1, d) for d in range(1,31)]
    data = data = [ random.random()*10 if (d > 15 and d < 20 or (d < 10 and d > 5)) else np.NaN for d in range(1,31)]
    
    df = pd.DataFrame(data, index = dt_ix, columns = ['Values'])
    
    df = df.ffill()