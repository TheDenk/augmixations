# -*- coding: utf-8 -*-

cutout_crop_rect_config = {
    'crop_x': (None, None),  #  Min max
    'crop_y': (None, None),
    'rect_h': (None, None),
    'rect_w': (None, None),
    'transparency': (0.0, 0.05),
    'hole_nums': (1, 1),
}

cutout_process_box_config = {
    'transp_box_visibility': 0.2,

    'max_overlap_area_ratio': 0.75,

    'min_height_result_ratio': 0.25,
    'min_width_result_ratio': 0.25,

    'max_height_intersection': 0.9,
    'max_width_intersection': 0.9,
}

cutmix_crop_rect_config = {
    'crop_x': (None, None),  #  Min max
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
