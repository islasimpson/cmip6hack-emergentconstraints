### Routine for correlation, linear regression and detrend
import xarray as xr
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt
%matplotlib inline


##correlation coefficient
def correlation (x,y)
    cor=np.corrcoef(x, y)
    return cor
    print('correlation:',cor)

## Testing -- generate random x and y
#  x is 1000 random integers between 0 and 50
#x = np.random.randint(0, 50, 100)
# y is same size as x, with positive Correlation with some noise
#y = x + np.random.normal(0, 10, 100)
# call it
#correlation(x,y)


## Linear regression
from sklearn.linear_model import LinearRegression

def linearregression(x,y):
    # transpose x
    x_t = np.array(x).reshape(-1,1)
    # Our linear model
    model = LinearRegression().fit(x_t, y)
    r_sq = model.score(x_t, y)
    print('intercept:', model.intercept_)
    print('slope:', model.coef_)
    print('coefficient of determination:', r_sq)
    # test plotting
    mn=np.min(x)
    mx=np.max(x)
    y1=model.coef_*x+model.intercept_
    plt.plot(x,y,'ob')
    plt.plot(x,y1,'-r')
#    plt.show()
    
    return model,model.intercept_,model.coef_,r_sq,plt

# call it
#linearregression(x,y)


## detrend func
from scipy import signal

def detrend(y):
    y_detrended = signal.detrend(y)
    return y_detrended
