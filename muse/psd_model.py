#!/usr/bin/env python
# -*- coding: utf-8 -*-

class PsdModel(object):
    def __init__(self, width, height, layers, name, path):
        self.width = width
        self.height = height
        self.layers = layers
        self.name = name
        self.path = path

        self.pm_left_point_x = None
        self.pm_right_point_x = None
        self.pm_left_point_y = None
        self.pm_right_point_y = None

    def get_char_layer(self):
        for layer in self.layers:
            if layer.name == 'char':
                return layer
        return None

    def get_char_light_layer(self):
        for layer in self.layers:
            if layer.name == 'char_light':
                return layer
        return None

    def get_slogan_layer(self):
        for layer in self.layers:
            if layer.name == 'slogan':
                return layer
        return None

    def get_slogan_light_layer(self):
        for layer in self.layers:
            if layer.name == 'slogan_light':
                return layer
        return None

    def get_logo_layer(self):
        for layer in self.layers:
            if layer.name == 'logo':
                return layer
        return None

    def get_bg_layer(self):
        for layer in self.layers:
            if layer.name == 'bg':
                return layer
        return None

    def get_button_layer(self):
        for layer in self.layers:
            if layer.name == 'butten' or layer.name == 'button':
                return layer
        return None

    def get_mask_layers(self):
        mask_layers = []
        for layer in self.layers:
            if layer.name.startswith('mask'):
                mask_layers.append(layer)
        return mask_layers

    def add_char_primary_area(self, pm_left_point_x, pm_right_point_x, pm_left_point_y, pm_right_point_y):
        # 注意位置是相对于主图左上作为原点的
        self.pm_left_point_x = pm_left_point_x
        self.pm_right_point_x = pm_right_point_x
        self.pm_left_point_y = pm_left_point_y
        self.pm_right_point_y = pm_right_point_y


