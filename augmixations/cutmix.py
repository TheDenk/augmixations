# -*- coding: utf-8 -*-
import numpy as np

from .configs import crop_rect_config_default, process_box_config_default


def generate_rect_coordinates(img_h: int, img_w: int,
                              min_x: int = None, min_y: int = None,
                              max_x: int = None, max_y: int = None,
                              min_h: int = None, min_w: int = None,
                              max_h: int = None, max_w: int = None):
    '''
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
    '''

    min_h = 1 if min_h is None else min_h
    min_w = 1 if min_w is None else min_w

    max_h = img_h if max_h is None else max_h
    max_w = img_w if max_w is None else max_w

    rect_h = np.random.randint(min_h, max_h)
    rect_w = np.random.randint(min_w, max_w)

    min_x = 0 if min_x is None or min_x < 0 else min_x
    min_y = 0 if min_y is None or min_x < 0 else min_y

    max_x = img_w - rect_w if max_x is None else max_x
    max_y = img_h - rect_h if max_y is None else max_y

    x1 = np.random.randint(min_x, max_x)
    x2 = x1 + rect_w if x1 + rect_w <= img_w else img_w

    y1 = np.random.randint(min_y, max_y)
    y2 = y1 + rect_h if y1 + rect_h <= img_h else img_h

    return x1, y1, x2, y2


def insert_image_in_background(bg_img: np.array, rect_img: np.array,
                               start_x: int, start_y: int,
                               min_x: int = None, min_y: int = None,
                               max_x: int = None, max_y: int = None,):
    """
    Description:
    Paste the cropped image into a RANDOM place on the background.

    Parameters:
    bg_img (np.array) - Background image for paste another image into
    rect_img (np.array) - Image which will be insert into background image
    start_x (int), start_y (int) - Default left top coordinates of inserted image for
    calculate differece between crop and insert position
    min_x (int), min_y (int) - Minimum allowed coordinates of the upper left point
    max_x (int), max_y (int) - Maximum allowed width and height of a rectangle

    Returns:
    (image, (shift_x, shift_y)) (np.array, (int, int)) - tuple of image and
        coordinates of shift inserted image
    """

    bg_h, bg_w, _ = bg_img.shape
    r_h, r_w, _ = rect_img.shape

    min_x = 0 if min_x is None else min_x
    max_x = bg_w - r_w if max_x is None else max_x

    min_y = 0 if min_y is None else min_y
    max_y = bg_h - r_h if max_y is None else max_y

    x1 = np.random.randint(min_x, max_x)
    x1 = bg_w - r_w if x1 + r_w >= bg_w else x1
    x2 = x1 + r_w

    y1 = np.random.randint(min_y, max_y)
    y1 = bg_h - r_h if y1 + r_h >= bg_h else y1
    y2 = y1 + r_h

    shift_x = x1 - start_x
    shift_y = y1 - start_y

    image = bg_img.copy()
    image[y1:y2, x1:x2] = rect_img

    return image, (shift_x, shift_y)


def shift_fg_rect_and_boxes(rect: np.array, boxes: np.array, shift_x: int, shift_y: int):
    """
    Description:
    The shift of the boxes is necessary after the cut image is inserted into
    a new random place on the background.
    Due to the fact that the starting and inserted places do not match,
    it is necessary to shift the boxes.

    Parameters:
    rect (np.array) - image rect coordinates
    boxes (np.array) - set of box coordinates
    shift_x (int) - X-axis shift
    shift_y (int) - Y-axis shift

    Returns:
    (new_rect, new_boxes) (np.array, np.array) - tuple of new image rectangle
        and box coordinates
    """
    x1, y1, x2, y2 = rect

    new_rect = np.array([
        x1 + shift_x,
        y1 + shift_y,
        x2 + shift_x,
        y2 + shift_y,
    ])

    new_boxes = boxes.copy()
    new_boxes[:, 0] += shift_x
    new_boxes[:, 1] += shift_y
    new_boxes[:, 2] += shift_x
    new_boxes[:, 3] += shift_y

    return new_rect, new_boxes


def check_middle_part_overlap_critical(rect_info: dict,
                                       box_info: dict,
                                       max_overlap_area_ratio: float,
                                       max_height_intersection: float,
                                       max_width_intersection: float,
                                       debug: bool = False,
                                       label: object = None,):
    """
    Description:
    Check for overlap of some central part of one of the sides of the box.

    Parameters:
    rect_info (dict) - dictionary with parameters of a rectangle that is cut from another picture
    box_info (dict) - a dictionary with boxing parameters which is possibly overridden
    max_overlap_area_ratio (float) - maximum box overlap threshold
    debug (bool) - debug output flag
    label (object) - the label of the current box to display in debug information

    Return:
    Boolean flag means that overlap exists and critical
    """
    r_x1, r_y1 = rect_info['x1'], rect_info['y1']
    r_x2, r_y2 = rect_info['x2'], rect_info['y2']

    image_rect_height = rect_info['height']
    image_rect_width = rect_info['width']
    image_rect_area = rect_info['area']

    b_x1, b_y1 = box_info['x1'], box_info['y1']
    b_x2, b_y2 = box_info['x2'], box_info['y2']

    new_box = np.array([b_x1, b_y1, b_x2, b_y2])

    start_box_height = box_info['height']
    start_box_width = box_info['width']
    start_box_area = box_info['area']

    top_img_side_in_box = r_y1 >= b_y1 and r_y1 <= b_y2
    bot_img_side_in_box = r_y2 >= b_y1 and r_y2 <= b_y2
    right_img_side_in_box = r_x2 >= b_x1 and r_x2 <= b_x2
    left_img_side_in_box = r_x1 >= b_x1 and r_x1 <= b_x2

    top_img_side_higher_box = r_y1 <= b_y1
    bot_img_side_lower_box = r_y2 >= b_y2

    left_img_side_left_box = r_x1 <= b_x1
    right_img_side_right_box = r_x2 >= b_x2

    overlap_full_middle_vertical = right_img_side_in_box and left_img_side_in_box and \
        top_img_side_higher_box and bot_img_side_lower_box

    overlap_full_middle_horizontal = top_img_side_in_box and bot_img_side_in_box and \
        left_img_side_left_box and right_img_side_right_box

    overlap_part_middle_left = right_img_side_in_box and left_img_side_left_box and \
        top_img_side_in_box and bot_img_side_in_box

    overlap_part_middle_right = left_img_side_in_box and right_img_side_right_box and \
        top_img_side_in_box and bot_img_side_in_box

    overlap_part_middle_top = bot_img_side_in_box and top_img_side_higher_box and \
        left_img_side_in_box and right_img_side_in_box

    overlap_part_middle_bot = top_img_side_in_box and bot_img_side_lower_box and \
        left_img_side_in_box and right_img_side_in_box

    if overlap_full_middle_vertical and overlap_full_middle_horizontal:
        overlap_part = image_rect_area / start_box_area
        if debug:
            print(f'{label} CRNTRAL MIDDLE OVERLAP')

    elif overlap_full_middle_vertical:
        overlap_area = start_box_height * image_rect_width
        overlap_part = overlap_area / start_box_area
        if debug:
            print(f'{label} FULL MIDDLE VERTICAL OVERLAP')

    elif overlap_full_middle_horizontal:
        overlap_area = start_box_width * image_rect_height
        overlap_part = overlap_area / start_box_area
        if debug:
            print(f'{label} FULL MIDDLE HORIZONTAL OVERLAP')

    elif overlap_part_middle_left:
        overlap_height = image_rect_height
        overlap_width = r_x2 - b_x1

        if overlap_height / start_box_height > max_height_intersection:
            new_box[0] = r_x2

        overlap_area = overlap_height * overlap_width
        overlap_part = overlap_area / start_box_area
        if debug:
            print(f'{label} PART MIDDLE LEFT HORIZONTAL OVERLAP')

    elif overlap_part_middle_right:
        overlap_height = image_rect_height
        overlap_width = b_x2 - r_x1

        if overlap_height / start_box_height > max_height_intersection:
            new_box[2] = r_x1

        overlap_area = overlap_height * overlap_width
        overlap_part = overlap_area / start_box_area
        if debug:
            print(f'{label} PART MIDDLE RIGHT HORIZONTAL OVERLAP')

    elif overlap_part_middle_top:
        overlap_height = r_y2 - b_y1
        overlap_width = image_rect_width

        if overlap_width / start_box_width > max_width_intersection:
            new_box[1] = r_y2

        overlap_area = overlap_height * overlap_width
        overlap_part = overlap_area / start_box_area
        if debug:
            print(f'{label} PART MIDDLE TOP VERTICAL OVERLAP')

    elif overlap_part_middle_bot:
        overlap_height = b_y2 - r_y1
        overlap_width = image_rect_width

        if overlap_width / start_box_width > max_width_intersection:
            new_box[3] = r_y1

        overlap_area = overlap_height * overlap_width
        overlap_part = overlap_area / start_box_area
        if debug:
            print(f'{label} PART MIDDLE BOT VERTICAL OVERLAP')
    else:
        return new_box, False

    return new_box, overlap_part > max_overlap_area_ratio


def correct_box_if_full_side_overlap(rect_info: dict, box_info: dict,
                                     max_overlap_area_ratio: float,
                                     debug: bool = False, label: object = None):
    """
    Description:
    Box verification for full side overlap case and correction it.
    Also checking overlap box area and return flag if overlap is critical.

    Parameters:
    rect_info (dict) - dictionary with parameters of a rectangle that is cut from another picture
    box_info (dict) - a dictionary with boxing parameters which is possibly overridden
    max_overlap_area_ratio (float) - maximum box overlap threshold
    debug (bool) - debug output flag
    label (object) - the label of the current box to display in debug information

    Return:
    (new_box, critical_overlap_flag) - correct box coordinates and Boolean flag means
        that overlap exists and critical
    """
    r_x1, r_y1 = rect_info['x1'], rect_info['y1']
    r_x2, r_y2 = rect_info['x2'], rect_info['y2']

    b_x1, b_y1 = box_info['x1'], box_info['y1']
    b_x2, b_y2 = box_info['x2'], box_info['y2']

    l_side_in_rect = (b_x1 >= r_x1 and b_x1 <= r_x2)
    r_side_in_rect = (b_x2 >= r_x1 and b_x2 <= r_x2)
    t_side_in_rect = (b_y1 >= r_y1 and b_y1 <= r_y2)
    b_side_in_rect = (b_y2 >= r_y1 and b_y2 <= r_y2)

    new_box = np.array([b_x1, b_y1, b_x2, b_y2])

    if l_side_in_rect and t_side_in_rect and b_side_in_rect:
        new_box[0] = r_x2
        if debug:
            print(f'{label} FULL LEFT SIDE OVERLAP')

    elif r_side_in_rect and t_side_in_rect and b_side_in_rect:
        new_box[2] = r_x1
        if debug:
            print(f'{label} FULL RIGHT SIDE OVERLAP')

    elif t_side_in_rect and r_side_in_rect and l_side_in_rect:
        new_box[1] = r_y2
        if debug:
            print(f'{label} FULL TOP SIDE OVERLAP')

    elif b_side_in_rect and r_side_in_rect and l_side_in_rect:
        new_box[3] = r_y1
        if debug:
            print(f'{label} FULL BOT SIDE OVERLAP')

    end_area = (new_box[3] - new_box[1]) * (new_box[2] - new_box[0])
    overlap_part = (box_info['area'] - end_area) / box_info['area']
    return new_box, overlap_part > max_overlap_area_ratio


def correct_box_if_some_alnge_overlap(rect_info: dict, box_info: dict,
                                      max_height_intersection: float,
                                      max_width_intersection: float,
                                      max_overlap_area_ratio: float,
                                      debug: bool = False, label: object = None):
    """
    Description:
    Box verification for some angle overlap case and correction it if some side overlap is critical.
    Also checking overlap box area and return flag if overlap is critical.

    Parameters:
    rect_info (dict) - dictionary with parameters of a rectangle that is cut from another picture
    box_info (dict) - a dictionary with boxing parameters which is possibly overridden
    max_height_intersection (float) - max part of height that should be exists or box will be changed
    max_width_intersection (float) - max part of width that should be exists or box will be changed
    max_overlap_area_ratio (float) - maximum box overlap threshold or box will be dropped
    debug (bool) - debug output flag
    label (object) - the label of the current box to display in debug information

    Return:
    (new_box, critical_overlap_flag) - correct box coordinates and Boolean flag means
        that overlap exists and critical
    """

    r_x1, r_y1 = rect_info['x1'], rect_info['y1']
    r_x2, r_y2 = rect_info['x2'], rect_info['y2']

    b_x1, b_y1 = box_info['x1'], box_info['y1']
    b_x2, b_y2 = box_info['x2'], box_info['y2']

    start_box_height = box_info['height']
    start_box_width = box_info['width']

    new_box = np.array([b_x1, b_y1, b_x2, b_y2])

    l_side_in_rect = (b_x1 >= r_x1 and b_x1 <= r_x2)
    r_side_in_rect = (b_x2 >= r_x1 and b_x2 <= r_x2)
    t_side_in_rect = (b_y1 >= r_y1 and b_y1 <= r_y2)
    b_side_in_rect = (b_y2 >= r_y1 and b_y2 <= r_y2)

    lt_in_rect = l_side_in_rect and t_side_in_rect
    lb_in_rect = l_side_in_rect and b_side_in_rect
    rt_in_rect = r_side_in_rect and t_side_in_rect
    rb_in_rect = r_side_in_rect and b_side_in_rect

    overlap_area = 0

    if lt_in_rect:
        if debug:
            print(f'{label} LEFT TOP OVERLAP')

        overlap_area = (r_x2 - b_x1) * (r_y2 - b_y1)

        tmp_height = new_box[3] - r_y2
        tmp_width = new_box[2] - r_x2

        bad_height = (1 - (tmp_height / start_box_height)) > max_height_intersection
        bad_width = (1 - (tmp_width / start_box_width)) > max_width_intersection

        if bad_height:
            new_box[0] = r_x2
        if bad_width:
            new_box[1] = r_y2

    elif rt_in_rect:
        if debug:
            print(f'{label} RIGHT TOP OVERLAP')

        overlap_area = (b_x2 - r_x1) * (r_y2 - b_y1)

        tmp_height = new_box[3] - r_y2
        tmp_width = r_x1 - new_box[0]

        bad_height = (1 - (tmp_height / start_box_height)) > max_height_intersection
        bad_width = (1 - (tmp_width / start_box_width)) > max_width_intersection

        if bad_height:
            new_box[2] = r_x1
        if bad_width:
            new_box[1] = r_y2

    elif rb_in_rect:
        if debug:
            print(f'{label} RIGHT BOT OVERLAP')

        overlap_area = (b_x2 - r_x1) * (b_y2 - r_y1)

        tmp_height = r_y1 - new_box[1]
        tmp_width = r_x1 - new_box[0]

        bad_height = (1 - (tmp_height / start_box_height)) > max_height_intersection
        bad_width = (1 - (tmp_width / start_box_width)) > max_width_intersection

        if bad_height:
            new_box[2] = r_x1
        if bad_width:
            new_box[3] = r_y1

    elif lb_in_rect:
        if debug:
            print(f'{label} LEFT BOT OVERLAP')

        overlap_area = (r_x2 - b_x1) * (b_y2 - r_y1)

        tmp_height = r_y1 - new_box[1]
        tmp_width = new_box[2] - r_x2

        bad_height = (1 - (tmp_height / start_box_height)) > max_height_intersection
        bad_width = (1 - (tmp_width / start_box_width)) > max_width_intersection

        if bad_height:
            new_box[1] = r_x2
        if bad_width:
            new_box[3] = r_y1

    end_box_area = box_info['area'] - overlap_area
    overlap_part = (box_info['area'] - end_box_area) / box_info['area']

    return new_box, overlap_part > max_overlap_area_ratio


def correct_background_boxes(bg_boxes: np.array,
                             bg_labels: np.array,
                             image_rect: np.array,
                             max_overlap_area_ratio: float,
                             min_height_ratio: float,
                             min_width_ratio: float,
                             max_height_intersection: float,
                             max_width_intersection: float,
                             debug: bool = False,
                             ):
    """
    Description:
    Background boxes correction by custom parameters.

    Parameters:
    bg_boxes (np.array) - background boxes coordinates
    bg_labels (np.array) - background labels of boxes
    image_rect (np.array) - coordinates of rectangle that will be inserted into background
    max_overlap_area_ratio (float) - maximum box overlap threshold. If overlap is larger - box will be dropped
    min_height_ratio (float) - min part of height that should be exists or box will be dropped
    min_width_ratio (float) - min part of width that should be exists or box will be dropped
    max_height_intersection (float) - max part of height that should be exists or box will be change
    max_width_intersection (float) - max part of width that should be exists or box will be change
    debug (bool) - debug output flag

    Return:
    (new_box, critical_overlap_flag) - correct box coordinates and Boolean flag means
        that overlap exists and critical
    """

    r_x1, r_y1, r_x2, r_y2 = image_rect

    rect_info = {
        'x1': r_x1,
        'y1': r_y1,
        'x2': r_x2,
        'y2': r_y2,
        'height': r_y2 - r_y1,
        'width': r_x2 - r_x1,
        'area': (r_y2 - r_y1) * (r_x2 - r_x1),
    }

    new_boxes = []
    new_labels = []

    for i, (box, label) in enumerate(zip(bg_boxes, bg_labels)):

        b_x1, b_y1, b_x2, b_y2 = box

        start_box_info = {
            'x1': b_x1,
            'y1': b_y1,
            'x2': b_x2,
            'y2': b_y2,
            'height': b_y2 - b_y1,
            'width': b_x2 - b_x1,
            'area': (b_y2 - b_y1) * (b_x2 - b_x1),
        }

        if b_x1 >= r_x1 and b_x2 <= r_x2 and b_y1 >= r_y1 and b_y2 <= r_y2:
            if debug:
                print(f'{label} TOTAL OVERLAP SKIP BY AREA')
            continue

        new_box, critical_overlap = check_middle_part_overlap_critical(
            rect_info, start_box_info,
            max_overlap_area_ratio,
            max_height_intersection,
            max_width_intersection,
            debug=debug,
            label=label)

        if critical_overlap:
            if debug:
                print('CRITICAL MIDLE PART OVERLAP')
            continue

        new_box, critical_overlap = correct_box_if_full_side_overlap(
            rect_info, start_box_info,
            max_overlap_area_ratio,
            debug=debug,
            label=label)

        if critical_overlap:
            if debug:
                print('CRITICAL FULL SIDE PART OVERLAP')
            continue

        new_box, critical_overlap = correct_box_if_some_alnge_overlap(
            rect_info, start_box_info,
            max_height_intersection,
            max_width_intersection,
            max_overlap_area_ratio,
            debug=debug,
            label=label)
        if critical_overlap:
            if debug:
                print('CRITICAL ANGLE PART OVERLAP')
            continue

        end_box_height = new_box[3] - new_box[1]
        end_box_width = new_box[2] - new_box[0]

        if (end_box_height / start_box_info['height']) < min_height_ratio:
            if debug:
                print('CRITICAL HEIGHT RATIO')
            continue
        if (end_box_width / start_box_info['width']) < min_width_ratio:
            if debug:
                print('CRITICAL WIDTH RATIO')
            continue

        new_boxes.append(new_box)
        new_labels.append(label)

    return new_boxes, new_labels


def correct_foreground_boxes(fg_boxes: np.array,
                             fg_labels: np.array,
                             image_rect: np.array,
                             max_overlap_area_ratio: np.array,
                             min_height_ratio: np.array,
                             min_width_ratio: np.array):
    """
    Description:
    Foreground boxes correction by custom parameters.

    Parameters:
    fg_boxes (np.array) - foreground boxes coordinates
    fg_labels (np.array) - foreground labels of boxes
    image_rect (np.array) - coordinates of rectangle that will be cutted from foreground
    max_overlap_area_ratio (float) - maximum box overlap threshold.
        If overlap is larger - box will be dropped
    min_height_ratio (float) - min part of height that should be exists or box will be dropped
    min_width_ratio (float) - min part of width that should be exists or box will be dropped

    Return:
    (new_box, critical_overlap_flag) - correct box coordinates and Boolean flag means
        that overlap exists and critical
    """
    x1, y1, x2, y2 = image_rect
    new_boxes = []
    new_labels = []

    # Поправляем боксы= вставленной картинки
    for i, (box, label) in enumerate(zip(fg_boxes, fg_labels)):
        f_x1, f_y1, f_x2, f_y2 = box
        start_box_height = f_y2 - f_y1
        start_box_width = f_x2 - f_x1

        l_side_in_rect = (f_x1 >= x1 and f_x1 <= x2)
        r_side_in_rect = (f_x2 >= x1 and f_x2 <= x2)
        t_side_in_rect = (f_y1 >= y1 and f_y1 <= y2)
        b_side_in_rect = (f_y2 >= y1 and f_y2 <= y2)

        # если какая-то часть бокса входит в новый прямоугольник
        if l_side_in_rect or r_side_in_rect or t_side_in_rect or b_side_in_rect:
            start_area = (f_x2 - f_x1) * (f_y2 - f_y1)
            # обрезаем части, которые вылезли за границу
            new_box = np.array([max(f_x1, x1), max(f_y1, y1), min(f_x2, x2), min(f_y2, y2)])

            end_box_height = new_box[3] - new_box[1]
            end_box_width = new_box[2] - new_box[0]
            end_box_area = end_box_height * end_box_width

            overlap_part = (start_area - end_box_area) / start_area

            if (end_box_height / start_box_height) < min_height_ratio:
                continue
            if (end_box_width / start_box_width) < min_width_ratio:
                continue
            if overlap_part > max_overlap_area_ratio:
                continue

            new_boxes.append(new_box)
            new_labels.append(label)
    return new_boxes, new_labels


def cutmix(bg_img: np.array,
           bg_boxes: np.array,
           bg_labels: np.array,

           fg_img: np.array,
           fg_boxes: np.array,
           fg_labels: np.array,

           crop_rect_config: dict = None,
           process_boxes_config: dict = None,
           ):
    """
    Description:
    Cutmix function. It function crop part of image from second image and paste it into first image.
    Function also changes first and second boxes and labels.

    Parameters:

    bg_img (np.array) - Background image. The image into which another image will be inserted.
    bg_boxes (np.array) - Boxes for background image.
    bg_labels (np.array) - Labels for background image.

    fg_img (np.array) - The image from which the rectangle will be cut
    fg_boxes (np.array) - Boxes for foreground image.
    fg_labels (np.array) - Labels for foreground image.

    crop_rect_config (dict) - Config with parameters of cut and insert coordinates
    process_boxes_config (dict) - Config with parameters of maximum box area overlap and maximum box side overlap
    Return:
    (new_image, new_boxes, new_labels) - New image, boxes and labels
    """
    cr_conf = crop_rect_config_default if crop_rect_config is None else crop_rect_config
    pb_conf = process_box_config_default if process_boxes_config is None else process_boxes_config

    img_h, img_w, _ = bg_img.shape

    fg_rect = generate_rect_coordinates(
        img_h=fg_img.shape[0], img_w=fg_img.shape[1],
        min_x=cr_conf['crop_min_x'], min_y=cr_conf['crop_min_y'],
        max_x=cr_conf['crop_max_x'], max_y=cr_conf['crop_max_y'],
        min_h=cr_conf['min_rect_h'], min_w=cr_conf['min_rect_w'],
        max_h=cr_conf['max_rect_h'], max_w=cr_conf['max_rect_w'],
    )

    x1, y1, x2, y2 = fg_rect
    cropped_img = fg_img[y1:y2, x1:x2]

    out_img, (shift_x, shift_y) = insert_image_in_background(
        bg_img, cropped_img, x1, y1,
        min_x=cr_conf['insert_min_x'], min_y=cr_conf['insert_min_y'],
        max_x=cr_conf['insert_max_x'], max_y=cr_conf['insert_max_y'],
    )

    fg_rect, fg_boxes = shift_fg_rect_and_boxes(fg_rect, fg_boxes, shift_x, shift_y)

    new_bg_boxes, new_bg_labels = correct_background_boxes(
        bg_boxes, bg_labels, fg_rect,
        pb_conf['max_overlap_area_ratio'],
        pb_conf['min_height_result_ratio'],
        pb_conf['min_width_result_ratio'],
        pb_conf['max_height_intersection'],
        pb_conf['max_width_intersection'],
        debug=True,
    )

    new_fg_boxes, new_fg_labels = correct_foreground_boxes(
        fg_boxes, fg_labels, fg_rect,
        pb_conf['max_overlap_area_ratio'],
        pb_conf['min_height_result_ratio'],
        pb_conf['min_width_result_ratio'],
    )

    return out_img, \
        np.array(new_bg_boxes + new_fg_boxes, dtype=np.float32), \
        np.array(new_bg_labels + new_fg_labels)
