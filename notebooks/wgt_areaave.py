import xarray as xr
import numpy as np

def wgt_areaave(ds,var,minlat,maxlat,minlon,maxlon):
    
    """
    calculates area-weighted average in rectangular region given by lat/lon on regular grid
    Args: ds (xarray.Dataset): dataset (needs to be 3-d, e.g. [time x lat x lon])
          var (str): variable to use
          minlat: -90..90
          maxlat: -90..90
          minlon: 0..360
          maxlon: 0..360
    Comment: cannot yet handle region crossing 0°...
    Import: from wgt_areaave import wgt_areaave as wa
    Usage: ts = wa(da,minlat,maxlat,minlon,maxlon)
    """
    
    # -- subsetting the data and latitudes
    subset = ds[var].where((minlon < ds.lon) & (ds.lon < maxlon) & (minlat < ds.lat) & (ds.lat < maxlat), drop=True)
    lats = ds.lat.where((minlat < ds.lat) & (ds.lat < maxlat), drop=True)
    # -- creating latitude weights
    lat_weights = np.cos(np.deg2rad(lats))
    # -- broadcasting weights to dimensions of data
    tmp1,tmp2 = xr.broadcast(lat_weights,subset,exclude=['lat'])
    weights = tmp1.transpose('time','lat','lon')
    # -- normalize weights
    weights = weights/np.sum(np.sum(weights,axis=1),axis=1)
    # -- apply weights and sum up
    ts = np.sum(np.sum((subset*weights),axis=1),axis=1)
    return (ts)