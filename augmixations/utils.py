# -*- coding: utf-8 -*-
import numpy as np


def generate_parameter(min_p, max_p, name=None):
    """
    Description:
    Checking parameters type and return the same type random parameter if min_p and max_p are not equals.
    If min_p == max_p it returns min_p.

    Parameters:
    min_p (int or float) - min parameter value
    max_p (int or float) - max parameter value
    name (str) - parameter name, using for error messaage

    Returns:
    x (int or float) -  random value between min_p and max_p
    """

    if min_p == max_p:
        return min_p

    elif isinstance(min_p, float) and isinstance(max_p, float):
        return np.random.uniform(min_p, max_p)

    elif isinstance(min_p, int) and isinstance(max_p, int):
        return np.random.randint(min_p, max_p)

    else:
        raise Exception(f'Generate random parameter {name} error. Set both type of parameters int or float.')


def unpack_mm_params(p):
    """
    Description:
    Unpacking parameter that can contains min and max values or single value.
    Checking type of input parameter for correctly process.
    Parameters:
    p (int or float or list or tuple) - single value or min and max values for some range

    Returns:
    (p1, p2) (tuple of int or tuple of float) - tuple of min and max values for some range
    """
    if isinstance(p, (tuple, list)):
        return p[0], p[1]
    elif isinstance(p, (int, float)):
        return p, p
    else:
        raise Exception('Unknown input parameter type.')
