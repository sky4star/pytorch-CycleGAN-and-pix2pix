import glob
import os

from PIL import Image
from os import path
from psd_tools import PSDImage
import cf as C

from muse.psd_parser import PsdParser


def scale(pil_img, max_size, method=Image.ANTIALIAS):
    """
    resize 'image' to 'max_size' keeping the aspect ratio
    and place it in center of white 'max_size' image
    """
    pil_img.thumbnail(max_size, method)
    offset = (int((max_size[0] - pil_img.size[0]) / 2), int((max_size[1] - pil_img.size[1]) / 2))
    back = Image.new("RGB", max_size, "white")
    back.paste(pil_img, offset)

    return back


def psd2png(psd_path, save_dir):
    psd = PSDImage.load(psd_path)
    psd = psd.as_PIL()
    psd_name = os.path.basename(psd_path)
    psd_name_without_extension = os.path.splitext(psd_name)[0]
    save_path = path.join(save_dir, psd_name_without_extension + '.png')
    psd.save(save_path)


# 特殊文件目录：佳佳
def batch_preprocess():
    max_size = (256, 256)
    save_folder = 'train_data/train'
    for artist in os.listdir(C.DATA_ROOT_PATH):
        if artist == '.DS_Store':
            continue
        root_path = os.path.join(C.DATA_ROOT_PATH, artist)
        for sub_dir in os.listdir(root_path):
            kv_dir = os.path.join(root_path, sub_dir + '/*.psd')
            jpg_dir = os.path.join(root_path, sub_dir + '/*/*.jpg')
            save_dir = os.path.join(C.DATA_ROOT_PATH, save_folder)

            # 主psd
            psd_info_list = []
            for psd_path in glob.glob(kv_dir):  # 处理配置中的通配符
                psd_info = PsdParser.parse_psd(psd_path)
                psd_info_list.append(psd_info)

            if len(psd_info_list) == 0:
                continue

            sorted_psd = sorted(psd_info_list, key=lambda _: (_.width * _.height))
            primary_kv_info = sorted_psd[-1]
            primary_kv = PSDImage.load(primary_kv_info.path).as_PIL()
            scaled_pkv = scale(primary_kv, max_size)

            # 合并其它的psd文件
            for psd_info in psd_info_list:
                if psd_info.path != primary_kv_info.path:
                    kv_img = PSDImage.load(psd_info.path).as_PIL()
                    scaled_jpg = scale(kv_img, max_size)

                    new_im = Image.new('RGB', (max_size[0] * 2, max_size[1]))
                    new_im.paste(scaled_pkv, (0, 0))
                    new_im.paste(scaled_jpg, (max_size[0], 0))

                    save_file_name = artist + '-' + sub_dir
                    save_file_name += '_{}x{}.png'.format(psd_info.width, psd_info.height)
                    save_path = path.join(save_dir, save_file_name)
                    new_im.save(save_path)
                    print('save ' + psd_info.path)

            # 读取jpg_dir目录的所有.jpg文件
            for jpg_path in glob.glob(jpg_dir):  # 处理配置中的通配符
                if jpg_path.find('/test') >= 0:
                    print('pass ' + jpg_path)
                    continue
                pil_img = Image.open(jpg_path)
                width = pil_img.size[0]
                height = pil_img.size[1]
                scaled_jpg = scale(pil_img, max_size)

                new_im = Image.new('RGB', (max_size[0]*2, max_size[1]))
                new_im.paste(scaled_pkv, (0, 0))
                new_im.paste(scaled_jpg, (max_size[0], 0))

                save_file_name = artist + '-' + sub_dir
                save_file_name += '_{}x{}.png'.format(width, height)
                save_path = path.join(save_dir, save_file_name)
                new_im.save(save_path)
                print('save ' + jpg_path)


if __name__ == "__main__":
    # psd_path = '/Users/sky4star/muse_test_data/董杉/2/1920-1080.ai.psd'
    # save_dir = '/Users/sky4star/muse_test_data/train_data'
    # if not path.exists(save_dir):
    #     os.makedirs(save_dir)
    # psd2png(psd_path, save_dir)

    # png_path = '/Users/sky4star/muse_test_data/train_data/1920-1080.ai.png'
    # pil_img = Image.open(png_path)
    # preprocessed = scale(pil_img, (1000, 600))
    # preprocessed.save('/Users/sky4star/muse_test_data/train_data/1920-1080_p.png', 'png')

    batch_preprocess()

