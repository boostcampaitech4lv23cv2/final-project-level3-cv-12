import os.path as osp
from os import listdir
from PIL import Image
from tqdm import tqdm
import numpy as np
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--PATH_IN', type=str, default='upper_body/temp_image_cloth_rmbkg', help="input dir")
    parser.add_argument('--PATH_OUT', type=str, default='upper_body/cloth_mask', help="output dir")
    parser.add_argument('--PATH_ID', type=str, default='upper_body/images', help="dir to get image ids")
    parser.add_argument('--THRESHOLD_VALUE', type=int, default=230, help="Threshold pixel value")
    
    args = parser.parse_args()
    return args


def get_mask(args):
    # 1. get ids
    files = listdir(args.PATH_ID)
    ids = []
    for file in files:
        if file[7] == '0':
            ids.append(file[:6])
    print(f'N images: {len(ids)}')

    # 2. from rmbkg, make mask
    for i in tqdm(ids):
        crop_pil = Image.open(osp.join(args.PATH_IN, i + '_1.png'))     # size 768x1024
        mask = np.transpose(np.array(crop_pil), (2, 0, 1))[3]           # (W H C) -> (C W H)

        mask0 = mask < args.THRESHOLD_VALUE
        mask[mask0] = 0
        mask[np.logical_not(mask0)] = 255

        mask = Image.fromarray(mask)
        mask.save(osp.join(args.PATH_OUT, i + '_7.jpg'))

if __name__=="__main__":
    print('Generate mask images from background_removed images')
    args = get_args()
    get_mask(args)
