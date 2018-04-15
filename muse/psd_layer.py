#!/usr/bin/env python
# -*- coding: utf-8 -*-

class PsdLayer(object):
    def __init__(self, width, height, x1, y1, x2, y2, name, image_path):
        self.width = width
        self.height = height
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.name = name
        self.image_path = image_path