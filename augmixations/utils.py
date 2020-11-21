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


def generate_rect_coordinates(img_h: int, img_w: int,
                              min_x: int = None, min_y: int = None,
                              max_x: int = None, max_y: int = None,
                              min_h: int = None, min_w: int = None,
                              max_h: int = None, max_w: int = None):
    """
    Description:
    Generation of coordinates by which the rectangle will be cut.

    Parameters:
    img_h (int), img_w (int) - Image parameters used to calculate the maximum value of a rectangle
    min_x (int), min_y (int) - Minimum allowed coordinates of the upper left point
    max_x (int), max_y (int) - Maximum allowed coordinates of the upper left point
    min_h (int), min_w (int) - Minimum allowed width and height of a rectangle
    max_h (int), max_w (int) - Maximum allowed width and height of a rectangle

    Returns:
    (x1, y1, x2, y2) (tuple of ints) -  Rectangle coordinates
    """
    # min_x, max_x = unpack_mm_params(x_param)
    # min_y, max_y = unpack_mm_params(y_param)
    # min_h, max_h = unpack_mm_params(rect_height)
    # min_w, max_w = unpack_mm_params(rect_width)

    min_h = img_h // 10 if min_h is None else min_h
    min_w = img_w // 10 if min_w is None else min_w

    max_h = img_h // 3 if max_h is None else max_h
    max_w = img_w // 3 if max_w is None else max_w

    rect_h = generate_parameter(min_h, max_h)
    rect_w = generate_parameter(min_w, max_w)

    min_x = 0 if min_x is None or min_x < 0 else min_x
    min_y = 0 if min_y is None or min_y < 0 else min_y

    max_x = img_w - rect_w if max_x is None else max_x
    max_y = img_h - rect_h if max_y is None else max_y

    x1 = generate_parameter(min_x, max_x)
    x2 = x1 + rect_w if x1 + rect_w <= img_w else img_w

    y1 = generate_parameter(min_y, max_y)
    y2 = y1 + rect_h if y1 + rect_h <= img_h else img_h

    return x1, y1, x2, y2
