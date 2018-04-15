#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psd_tools import PSDImage
import numpy as np
from PIL import Image
import os
import pathlib

# 读取psd文件，获取指定层信息，保存指定层图片
from muse.psd_layer import PsdLayer
from muse.psd_model import PsdModel


class PsdParser:
    """
    读取path指向的PSD文件，获取图层信息并保存图层至相应名称的PNG图片；
    """
    @staticmethod
    def parse_psd(path):
        psd_name = os.path.basename(path)
        psd_name_without_extension = os.path.splitext(psd_name)[0]
        dir_path = os.path.dirname(path)
        layer_save_path = os.path.join(dir_path, psd_name_without_extension)
        pathlib.Path(layer_save_path).mkdir(parents=True, exist_ok=True)

        psd = PSDImage.load(path)
        header = psd.header
        layers = psd.layers

        layer_infos = []
        for layer in layers:
            save_path = os.path.join(layer_save_path, layer.name + '.png')

            m_x1 = 0
            m_y1 = 0

            if not os.path.exists(save_path):
                try:
                    layerPIL = layer.as_PIL()
                    if layer.name.find("_light") > 0:
                        layerPIL = PsdParser.remove_black_from_light_layer(layerPIL)
                    layerPIL, m_x1, m_y1 = PsdParser.trim(layerPIL)
                    if layerPIL is not None:
                        try:
                            layerPIL.save(save_path)
                        except RuntimeError:
                            print('RuntimeError: Saving layer png failed', save_path)
                        except TypeError:
                            print('TypeError: Saving layer png failed', save_path)
                        except NameError:
                            print('NameError: Saving layer png failed', save_path)
                        except ValueError:
                            print('ValueError: Saving layer png failed', save_path)
                except ValueError:
                    print('RuntimeError: Parsing layer failed', layer.name)

            layer_info = PsdLayer(layer.bbox.width, layer.bbox.height,
                                  layer.bbox.x1 + m_x1, layer.bbox.y1 + m_y1, layer.bbox.x2, layer.bbox.y2,
                                  layer.name, save_path)
            layer_infos.append(layer_info)

        psd_info = PsdModel(header.width, header.height, layer_infos, psd_name, path)
        return psd_info

    @staticmethod
    def remove_black_from_light_layer(layerPIL):
        """
        对于需要通过滤色的混合选项(screen blend)的图层，纯黑不透明(alpha==100%)的部分可以扔掉
        :param layerPIL: 原图层PIL
        :return: 去黑图层PIL
        """
        pixel = layerPIL.load()

        for y in range(layerPIL.size[1]):
            for x in range(layerPIL.size[0]):
                if pixel[x, y][0] == 0 and pixel[x, y][1] == 0 and pixel[x, y][2] == 0 and pixel[x, y][3] == 255:
                    pixel[x, y] = (0, 0, 0, 0)

        return layerPIL

def main():
    print(os.path.dirname(os.path.realpath(__file__)))
    # psd = PsdParser.parse_psd('/Users/sky4star/Github/muse/data/test/psd/600-600.ai.psd')
    psd = PsdParser.parse_psd('C:/workroot/DataTeam/lab/python/muse/image_src/768-1024.ai.psd')


if __name__ == "__main__":
    main()
