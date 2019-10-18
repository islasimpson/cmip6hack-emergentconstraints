import geopandas as gpd
import regionmask

def read_state(file, statename):
    """ read and select state from file
    Args: 
       file (str): path to state shapefile
       statename (str): name of state (i.e. California)
    """
    all = gpd.read_file("../data/states.shp")

    state = all[all['STATE_NAME'] == statename]
    return state

def state_mask(state, ds, name, abbr):
    """
    create mask from a geodataframe
    Args:
       state (geodataframe): state to use
       ds (xarray.DataArray): DataArray with coords to match
       name (str): name of state
       abbr (str): abbreviation of state
       """
    number = [0]
    region = regionmask.Regions_cls('statemask', number, [name], [abbr], state.geometry.values)
    mask = region.mask(ds, wrap_lon=True) + 1
    
    return mask