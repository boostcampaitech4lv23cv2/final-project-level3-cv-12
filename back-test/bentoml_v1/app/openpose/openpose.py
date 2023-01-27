import cv2
import matplotlib.pyplot as plt
import copy
import numpy as np
import os
import argparse
import json

import model
import openpose.util
from openpose.body import Body

class Openpose:
    def __init__(self, model):
        self.body_estimation = Body(model)

    def save_bodypose(self, image_bgr, out_dir, filename):
        skeleton, keypoint = self.get_bodypose(image_bgr)
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        cv2.imwrite(os.path.join(out_dir, filename), skeleton)
        with open(os.path.join(out_dir, filename.replace('.jpg', '.json')), "w") as json_file:
            json.dump(keypoint, json_file)

    def get_bodypose(self, image_bgr):
        candidate, subset = self.body_estimation(image_bgr)
        keypoint = {}
        keypoint['keypoints'] = candidate.tolist()
        canvas = np.zeros(image_bgr.shape)
        skeleton = util.draw_bodypose(canvas, candidate, subset)
        return skeleton, keypoint

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_img', type=str, default='./images/demo.jpg', required=True)
    parser.add_argument('--out_dir', type=str, default='./results', help='directory path to save results')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    image_bgr = cv2.imread(args.input_img)  # B,G,R order
    openpose= Openpose()
    openpose.save_bodypose(image_bgr, args.out_dir, os.path.basename(args.input_img))