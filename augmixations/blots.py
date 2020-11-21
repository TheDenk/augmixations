# -*- coding: utf-8 -*-
import numpy as np

from .utils import generate_rect_coordinates, unpack_mm_params, generate_parameter


class HandWrittenBlot:
    def __init__(self, height, width, incline, intensivity, transparency, count):
        try:
            import cv2
        except ImportError:
            raise Exception('OpenCV not found. Please install it. Run command: pip install opencv-python>=4.1.1')

        try:
            import bezier
        except ImportError:
            raise Exception('Bezier not found. Please install it. Run command: pip install bezier>=2020.5.19')

        self.cv2 = cv2
        self.bezier = bezier

        self.min_h, self.max_h = unpack_mm_params(height)
        self.min_w, self.max_w = unpack_mm_params(width)
        self.min_incline, self.max_incline = unpack_mm_params(incline)
        self.min_intens, self.max_intens = unpack_mm_params(intensivity)
        self.min_transp, self.max_transp = unpack_mm_params(transparency)
        self.count = count

    def generate_points(self, mask_x, mask_y, mask_w, mask_h, intensivity, incline):
        points_count = int(intensivity * 20)

        point_prer_pixel = points_count / mask_h
        step_size = int(1 / point_prer_pixel) if 1 / point_prer_pixel > 1 else 1

        lp_min, lp_max = int(mask_w*0.01), int(mask_w*0.20)
        rp_min, rp_max = int(mask_w*0.8), int(mask_w*0.99)

        points = [[], []]

        for i, step in enumerate(range(0, points_count*step_size, step_size)):

            if i < points_count // 10:
                x = np.random.randint(mask_x, mask_x + mask_w)
                y = np.random.randint(mask_y, mask_y + mask_h)
                points[0].append(x)
                points[1].append(y)
            else:
                l_att = np.random.randint(10, 80)
                r_att = 80 - l_att

                if i % 2 == 0:
                    for _ in range(l_att):
                        x = np.random.randint(lp_min, lp_max)
                        y = np.random.randint(step + incline, step + step_size + incline)

                        points[0].append(x + mask_x)
                        points[1].append(y + mask_y)
                else:
                    for _ in range(r_att):
                        x = np.random.randint(rp_min, rp_max)
                        y = np.random.randint(step - incline, step + step_size - incline)

                        points[0].append(x + mask_x)
                        points[1].append(y + mask_y)

        return points

    def draw_bezier_curve(self, image, points):
        img = image.copy()

        curve = self.bezier.Curve(points, degree=len(points[0]) - 1)

        x, y = curve.evaluate(0.01)
        x1, y1 = int(x), int(y)

        for point in np.arange(0.01, 0.99, 0.02):
            x, y = curve.evaluate(point)
            x2, y2 = int(x), int(y)
            img = self.cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), np.random.randint(1, 5))
            x1, y1 = x2, y2

        return img

    def make_handwriting(self, image, configs):
        bg_img = image.copy()
        fg_img = image.copy()

        for config in configs:
            for _ in range(config['repeat']):
                points = self.generate_points(
                    config['x'],
                    config['y'],
                    config['w'],
                    config['h'],
                    config['points_intensivity'],
                    config['incline'],
                )
                fg_img = self.draw_bezier_curve(fg_img, points)

            bg_img = self.cv2.addWeighted(bg_img, config['transparency'], fg_img, 1 - config['transparency'], 0)

        return bg_img

    def generate_configs(self, img_h, img_w):

        configs = []

        for _ in range(self.count):

            x1, y1, x2, y2 = generate_rect_coordinates(img_h=img_h, img_w=img_w)

            incline = generate_parameter(self.min_incline, self.max_incline, 'incline')
            intensivity = generate_parameter(self.min_intens, self.max_intens, 'intensivity')
            transp = generate_parameter(self.min_transp, self.max_transp, 'transparency')

            configs.append({
                'x': x1,
                'y': y1,
                'w': x2 - x1,
                'h': y2 - y1,
                'points_intensivity': intensivity,
                'repeat': int(intensivity * 5),
                'transparency': transp,
                'incline': incline,
            })

        return configs

    def apply(self, image):
        img_h, img_w, _ = image.shape
        shades_configs = self.generate_configs(img_h, img_w)
        img = self.make_handwriting(image, shades_configs)
        return img
