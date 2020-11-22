# -*- coding: utf-8 -*-

blot_rect_config = {
    'x': (None, None),
    'y': (None, None),
    'h': (None, None),
    'w': (None, None),
}

blot_params = {
    'incline': (-10, 10),
    'intensivity': (0.5, 0.9),
    'transparency': (0.05, 0.4),
    'count': 1,
}


cutmix_crop_rect_config = {
    'crop_x': (None, None),
    'crop_y': (None, None),
    'rect_h': (None, None),
    'rect_w': (None, None),
    'insert_x': (None, None),
    'insert_y': (None, None),
}

cutmix_process_box_config = {
    'max_overlap_area_ratio': 0.75,

    'min_height_result_ratio': 0.25,
    'min_width_result_ratio': 0.25,

    'max_height_intersection': 0.9,
    'max_width_intersection': 0.9,
}
