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
    Usage example: ts = wa(ds,'ts',minlat,maxlat,minlon,maxlon)
    """
    
    # -- subsetting the data and latitudes
    subset = ds[var].where((minlon < ds.lon) & (ds.lon < maxlon) & (minlat < ds.lat) & (ds.lat < maxlat), drop=True)
    lats = ds.lat.where((minlat < ds.lat) & (ds.lat < maxlat), drop=True)
    # -- creating latitude weights
    lat_weights = np.cos(np.deg2rad(lats))
    
    # -- broadcasting weights to dimensions of data 
    weights = xr.broadcast(lat_weights,subset,exclude=['lat'])
    # -- normalize weights (divide by sum of all lat/lon weights within each dim)
    norm_weights = weights[0]/weights[0].sum(dim=("lat", "lon"))
    # -- apply weights and sum up
    ts = (subset*norm_weights).sum(dim=("lat", "lon"))
    return (ts)