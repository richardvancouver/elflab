######################################################################################################
# various methods for estimating errors
######################################################################################################

import numpy as np

# returns an estimator that always gives a fixed value for error
def fixed(error_value):
    def f(*args, **kwargs):
        return error_value
    return f
    

# an estimator that gives standard deviation as error
def std(values, errors):
    """takes two numpy arrays: values and errors in these values
    estimate the grand standard deviation as error value
    not accurate for multiple rounds of averaging"""
    var1 = np.nanvar(values, ddof=1)    # variance in the values
    var2 = np.nanmean(np.square(errors)) # mean-square of input errors
    return np.sqrt(var1 + var2)
    
# standard error of the mean
def se(values, errors=None):
    n = values.size
    if n <= 1:
        raise ValueError
    st = np.nanstd(values)
    se = st / sqrt(n-1)
    
    
# an estimator that gives median value of the input errors as error
def median(values, errors):
    """takes two numpy arrays: values and errors in these values
    estimate the grand standard deviation as error value
    not accurate for multiple rounds of averaging"""
    return np.median(errors)