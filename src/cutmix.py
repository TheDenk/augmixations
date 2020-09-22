import numpy as np

from .configs import crop_rect_config_default, process_bos_config_default


def generate_rect_coordinates(fg_image,
                  min_x, min_y, max_x, max_y, 
                  min_h, min_w, max_h, max_w):
    '''
    Генерация координат по которым будет вырезан прямоугольник 
    для вставки в бекграунд.
    '''
    img_h, img_w, img_c = fg_image.shape
    
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

def insert_image_in_background(bg_img, fg_img, start_crop_position,
                               min_x=None, min_y=None,
                               max_x=None, max_y=None,):
    """
    Вставляем кропнутую карнинку в РАНДОМНОЕ место на бекграунде.
    """
    bg_h, bg_w, _ = bg_img.shape
    fg_h, fg_w, _ = fg_img.shape
    
    start_x = start_crop_position[0]
    start_y = start_crop_position[1]
    
    min_x = 0 if min_x is None else min_x
    max_x = bg_w - fg_w if max_x is None else max_x
    
    
    min_y = 0 if min_y is None else min_y
    max_y = bg_h - fg_h if max_y is None else max_y
    
    x1 = np.random.randint(min_x, max_x)
    x1 = bg_w - fg_w if x1 + fg_w >= bg_w else x1
    x2 = x1 + fg_w
    
    y1 = np.random.randint(min_y, max_y) 
    y1 = bg_h - fg_h if y1 + fg_h >= bg_h else y1
    y2 = y1 + fg_h
    
    shift_x = x1 - start_x
    shift_y = y1 - start_y
    
    image = bg_img.copy()
    image[y1:y2, x1:x2] = fg_img
    
    return image, (shift_x, shift_y)

def shift_fg_rect_and_boxes(rect:np.array, boxes:np.array, shift_x:int, shift_y:int):
    """
    Сдвиг боксов необходим после того как вырезанную картинку 
    вставляем в новое рандомное место на бекграунде. 
    Из за того, что начальное и вставленное места не совпадают необходим сдвиг боксов.
    rect: np.array, исходные координаты прямоугольника для кропа
    boxes: np.array, набор координат боксов
    shift_x:int: сдвиг по оси X
    shift_y:int: сдвиг по оси Y
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

def check_middle_part_overlap_critical(rect_info:dict, 
                                    box_info:dict, 
                                    max_overlap_area_ratio:float, 
                                    debug:bool=False, 
                                    label:object=None,):
    """
    Проверка на перекрытие какой-то центральной части одной из сторон бокса.
    rect_info: dict, словарь с параметрами прямоугольника который вырезан из другой картинки
    box_info: dict, словарь с параметрами бокса который, возможно, перекрыт
    max_overlap_area_ratio: порог максимального перекрытия бокса
    debug: флаг вывода отладочной информации
    label: класс текущего бокса, для отображения в отладочной информации
    """
    r_x1, r_y1 = rect_info['x1'], rect_info['y1']
    r_x2, r_y2 = rect_info['x2'], rect_info['y2']
    
    image_rect_height = rect_info['height']
    image_rect_width = rect_info['width']
    image_rect_area = rect_info['area']
    
    b_x1, b_y1 = box_info['x1'], box_info['y1']
    b_x2, b_y2 = box_info['x2'], box_info['y2']
    
    start_box_height = box_info['height']
    start_box_width = box_info['width']
    start_box_area = box_info['area']
    
    top_img_side_in_box = r_y1 >= b_y1 and r_y1 <= b_y2
    bot_img_side_in_box = r_y2 >= b_y1 and r_y2 <= b_y2
    right_img_side_in_box = r_x2 >= b_x1 and r_x2 <= b_x2
    left_img_side_in_box = r_x1 >= b_x1 and r_x1 <= b_x2

    top_img_side_higher_box = r_y1 <= b_y1
    bot_img_side_higher_box = r_y2 <= b_y1

    top_img_side_lower_box = r_y1 >= b_y2
    bot_img_side_lower_box = r_y2 >= b_y2

    left_img_side_left_box = r_x1 <= b_x1
    right_img_side_left_box = r_x2 <= b_x1

    left_img_side_right_box = r_x1 >= b_x2
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

    if overlap_full_middle_vertical and overlap_full_midle_horizontal:
        overlap_part = image_rect_area / start_box_area
        if debug:
            print(f'{label} MIDLE MIDDLE OVERLAP')
        
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
        overlap_area = overlap_height * overlap_width
        overlap_part = overlap_area / start_box_area
        if debug:
            print(f'{label} PART MIDDLE LEFT HORIZONTAL OVERLAP')

    elif overlap_part_middle_right:
        overlap_height = image_rect_height
        overlap_width = b_x2 - r_x1 
        overlap_area = overlap_height * overlap_width
        overlap_part = overlap_area / start_box_area
        if debug:
            print(f'{label} PART MIDDLE RIGHT HORIZONTAL OVERLAP')

    elif overlap_part_middle_top:
        overlap_height = r_y2 - b_y1
        overlap_width = image_rect_width
        overlap_area = overlap_height * overlap_width
        overlap_part = overlap_area / start_box_area
        if debug:
            print(f'{label} PART MIDDLE TOP VERTICAL OVERLAP')

    elif overlap_part_middle_bot:
        overlap_height = b_y2 - r_y1
        overlap_width = image_rect_width
        overlap_area = overlap_height * overlap_width
        overlap_part = overlap_area / start_box_area
        if debug:
            print(f'{label} PART MIDDLE BOT VERTICAL OVERLAP')
    else:
        return False
      
    return overlap_part > max_overlap_area_ratio

def correct_box_if_full_side_overlap(rect_info, box_info, max_overlap_area_ratio, debug=False, label=None):
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

def correct_box_if_some_alnge_overlap(rect_info, box_info,
                                     min_height_when_overlap_ratio,
                                     min_width_when_overlap_ratio,
                                     max_overlap_area_ratio,
                                     debug=False, label=None):
    r_x1, r_y1 = rect_info['x1'], rect_info['y1']
    r_x2, r_y2 = rect_info['x2'], rect_info['y2']
    
    image_rect_height = rect_info['height']
    image_rect_width = rect_info['width']
    image_rect_area = rect_info['area']
    
    b_x1, b_y1 = box_info['x1'], box_info['y1']
    b_x2, b_y2 = box_info['x2'], box_info['y2']
    
    start_box_height = box_info['height']
    start_box_width = box_info['width']
    start_box_area = box_info['area']
    
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
        
        overlap_area = (r_x2 -  b_x1) * (r_y2 - b_y1)
        
        tmp_height = new_box[3] - r_y2
        tmp_width = new_box[2] - r_x2

        bad_height = (tmp_height / start_box_height) < min_height_when_overlap_ratio
        bad_width = (tmp_width / start_box_width) < min_width_when_overlap_ratio

        if bad_height:
            new_box[0] = r_x2
        if bad_width:
            new_box[1] = r_y2

    elif rt_in_rect:
        if debug:
            print(f'{label} RIGHT TOP OVERLAP')
        
        overlap_area = (b_x2 -  r_x1) * (r_y2 - b_y1)
        
        tmp_height = new_box[3] - r_y2 
        tmp_width = r_x1 - new_box[0]

        bad_height = (tmp_height / start_box_height) < min_height_when_overlap_ratio
        bad_width = (tmp_width / start_box_width) < min_width_when_overlap_ratio

        if bad_height:
            new_box[2] = r_x1
        if bad_width:
            new_box[1] = r_y2

    elif rb_in_rect:
        if debug:
            print(f'{label} RIGHT BOT OVERLAP')
            
        overlap_area = (b_x2 -  r_x1) * (b_y2 - r_y1)

        tmp_height = r_y1 - new_box[1]
        tmp_width = r_x1 - new_box[0]

        bad_height = (tmp_height / start_box_height) < min_height_when_overlap_ratio
        bad_width = (tmp_width / start_box_width) < min_width_when_overlap_ratio

        if bad_height:
            new_box[2] = r_x1
        if bad_width:
            new_box[3] = r_y1

    elif lb_in_rect:
        if debug:
            print(f'{label} LEFT BOT OVERLAP')
            
        overlap_area = (r_x2 -  b_x1) * (b_y2 - r_y1)

        tmp_height = r_y1 - new_box[1] 
        tmp_width = new_box[2] - r_x2

        bad_height = (tmp_height / start_box_height) < min_height_when_overlap_ratio
        bad_width = (tmp_width / start_box_width) < min_width_when_overlap_ratio

        if bad_height:
            new_box[1] = r_x2
        if bad_width:
            new_box[3] = r_y1
    
    end_area = (new_box[3] - new_box[1]) * (new_box[2] - new_box[0])
    end_box_area = box_info['area'] - overlap_area
    overlap_part = (box_info['area'] - end_box_area) / box_info['area']
        
    return new_box, overlap_part > max_overlap_area_ratio
    
def correct_background_boxes(bg_boxes,  # Боксы бэкграунда
                             bg_labels, # Лейблэ бэкграунда
                             image_rect, # Координаты новой картинки
                             max_overlap_area_ratio, # Порог перекрытия бокса, если перекрытие больше этого порога, то бокс выбрасывается
                             min_height_ratio, # Минимальный коэффициент результирующего бокса. Если новая высота, подленная на старую меньше этого порога то бокс выбрасывается
                             min_width_ratio,
                             min_height_when_overlap_ratio, # Минимальный коэфициент, при перекрытии угла бокса. Если отношение новой высоты к старой меньше данного коэффициента, то бокс обрезается
                             min_width_when_overlap_ratio,
                             debug=True,
                             ):
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
        
        # Перекрытия бывают четырёх видов: 
        #   1) перекрытие бокса полностью;
        #   2) перекрыта сторона полностью;
        #   3) перекрыта сторона где-то по центру;
        #   4) перекрыт угол;
        # достаточно обработать только один случай
        
        # Если бокс полностью перекрыт новой картинкой выбрасываем
        if b_x1 >= r_x1 and b_x2 <= r_x2 and b_y1 >= r_y1 and b_y2 <= r_y2:
            if debug:
                print(f'{label} TOTAL OVERLAP SKIP BY AREA')
            continue
        
        critical_overlap = check_middle_part_overlap_critical(
                                              rect_info, start_box_info, 
                                              max_overlap_area_ratio, 
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
                                                    min_height_when_overlap_ratio,
                                                    min_width_when_overlap_ratio,
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

def correct_foreground_boxes(fg_boxes, fg_labels, rect, max_overlap_area_ratio, min_height_ratio, min_width_ratio):
    x1, y1, x2, y2 = rect
    new_boxes = []
    new_labels = []
    
    # Поправляем боксы= вставленной картинки
    for i, (box, label) in enumerate(zip(fg_boxes, fg_labels)):
        f_x1, f_y1, f_x2, f_y2 = box
        start_box_height = f_y2 - f_y1
        start_box_width = f_x2 - f_x1
        start_box_area = start_box_height * start_box_width
        
        l_side_in_rect = (f_x1 >= x1 and f_x1 <= x2)
        r_side_in_rect = (f_x2 >= x1 and f_x2 <= x2)
        t_side_in_rect = (f_y1 >= y1 and f_y1 <= y2)
        b_side_in_rect = (f_y2 >= y1 and f_y2 <= y2)
        
        # если какая-то часть бокса входит в новый прямоугольник
        if l_side_in_rect or r_side_in_rect or t_side_in_rect or b_side_in_rect:
            start_area = (f_x2 - f_x1) * (f_y2 - f_y1)
            #обрезаем части, которые вылезли за границу
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


def cutmix(bg_img:np.array, 
           bg_boxes:np.array,
           bg_labels:np.array,
           
           fg_img:np.array, 
           fg_boxes:np.array,
           fg_labels:np.array,
           
           crop_rect_config=None,
           process_boxes_config=None,
           ):
    
    cr_conf = crop_rect_config_default if crop_rect_config is None else crop_rect_config
    pb_conf = process_box_config_default if process_boxes_config is None else process_boxes_config
    
    img_h, img_w, _ = bg_img.shape
    
    max_rect_h = img_h if cr_conf['max_rect_h'] is None else cr_conf['max_rect_h']
    max_rect_w = img_w if cr_conf['max_rect_w'] is None else cr_conf['max_rect_w']
    
    fg_rect = generate_rect_coordinates(fg_img, 
                                      min_x=cr_conf['crop_min_x'], min_y=cr_conf['crop_min_y'],
                                      max_x=cr_conf['crop_max_x'], max_y=cr_conf['crop_max_y'], 
                                      min_h=cr_conf['min_rect_h'], min_w=cr_conf['min_rect_w'], 
                                      max_h=cr_conf['max_rect_h'], max_w=cr_conf['max_rect_w'],
                                        )
    
    x1, y1, x2, y2 = fg_rect
    cropped_img = fg_img[y1:y2, x1:x2]
    start_crop_position = (x1, y1)
    
    out_img, (shift_x, shift_y) = insert_image_in_background(bg_img, cropped_img, start_crop_position,
                                         min_x=cr_conf['insert_min_x'], min_y=cr_conf['insert_min_y'],
                                         max_x=cr_conf['insert_max_x'], max_y=cr_conf['insert_max_y'],
                                        )
    
    fg_rect, fg_boxes = shift_fg_rect_and_boxes(fg_rect, fg_boxes, shift_x, shift_y)

    new_bg_boxes, new_bg_labels = correct_background_boxes(bg_boxes, bg_labels, fg_rect, 
                                            pb_conf['max_overlap_area_ratio'], 
                                            pb_conf['min_height_ratio'],
                                            pb_conf['min_width_ratio'],
                                            pb_conf['min_height_when_overlap_ratio'],
                                            pb_conf['min_width_when_overlap_ratio'],
                                            debug=True,
                                           )
    
    new_fg_boxes, new_fg_labels = correct_foreground_boxes(fg_boxes, fg_labels, fg_rect, 
                                        pb_conf['max_overlap_area_ratio'], 
                                        pb_conf['min_height_ratio'], 
                                        pb_conf['min_width_ratio'],
                                       )
    
    return out_img, \
           np.array(new_bg_boxes + new_fg_boxes, dtype=np.float32), \
           np.array(new_bg_labels + new_fg_labels)