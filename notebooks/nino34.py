import xarray as xr
import numpy as np
import numpy.ma as ma
import matplotlib as plt
import matplotlib.pyplot as plt
import os
import cftime
import nc_time_axis
import numpy.matlib
from season_util import season_mean
from wgt_areaave import wgt_areaave as wa

def nino34(ds,var,seas):
    
    """
    calculates Nino 3.4 from monthly mean gridded data
    Args: ds (xarray.Dataset): dataset (needs to be 3-d, e.g. [time x lat x lon])
          var (str): variable to use
          seas (str): season to calculate Nino 3.4 for
                      (options: 'monthly'-->no seasonal average, returns monthly means; 'DJF'; 'MAM'; JJA'; 'SON')
    Comment: 
    Import: from nino34 import nino34
    Usage example: nino = nino34(da,'ts','DJF')
    """
    
    minlat = -5
    maxlat = 5
    minlon = -170+360
    maxlon = -120+360
    
    nino = wa(ds,'ts',minlat,maxlat,minlon,maxlon)

    if seas == 'monthly':
        pass
    else:
        nino = nino.where(nino['time.season'] == seas)
        nino = nino.rolling(min_periods=3, center=True, time=3).mean()
        nino = nino.groupby('time.year').mean('time')

    # -- normalize
    nino = (nino-np.mean(nino))/np.std(nino)
        
    return (nino)