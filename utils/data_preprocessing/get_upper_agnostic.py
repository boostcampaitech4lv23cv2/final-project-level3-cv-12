import json
from os import path as osp
import os

import numpy as np
from PIL import Image, ImageDraw

import argparse
from tqdm import tqdm


def get_img_agnostic_onlypose(img, pose_data):
    for pair in [[3,4], [6,7]]:
        pointx, pointy = pose_data[pair[1]]+(pose_data[pair[1]]-pose_data[pair[0]])*0.3
        pointx, pointy = int(pointx), int(pointy)

    r = 10
    img = np.array(img)
    img = Image.fromarray(img)
    agnostic = img.copy()
    agnostic_draw = ImageDraw.Draw(agnostic)

    # 골반 위치 조정
    length_a = np.linalg.norm(pose_data[5] - pose_data[2]+1e-8)
    length_b = np.linalg.norm(pose_data[11] - pose_data[8]+1e-8)
    point = (pose_data[8] + pose_data[11]) / 2
    pose_data[8] = point + (pose_data[8] - point) / length_b * length_a
    pose_data[11] = point + (pose_data[11] - point) / length_b * length_a

    # mask line shoulder
    agnostic_draw.line([tuple(pose_data[i]) for i in [2, 5]], 'black', width=r*3)

    # mask circle shoulder
    for i in [2, 5]:
        pointx, pointy = pose_data[i]
        agnostic_draw.ellipse((pointx-r*4, pointy-r*4, pointx+r*4, pointy+r*4), 'black', 'black')

    # mask arm
    for i in [3, 4, 6, 7]:
        if (pose_data[i - 1, 0] < 0.0 and pose_data[i - 1, 1] < 0.0) or (pose_data[i, 0] < 0.0 and pose_data[i, 1] < 0.0):
            continue
        agnostic_draw.line([tuple(pose_data[j]) for j in [i - 1, i]], 'black', width=r*10)
        pointx, pointy = pose_data[i]
        if i in [4, 7]:
            pass    #agnostic_draw.ellipse((pointx-r, pointy-r, pointx+r, pointy+r), 'black', 'black')
        else:
            agnostic_draw.ellipse((pointx-r*4, pointy-r*4, pointx+r*4, pointy+r*4), 'black', 'black')

    # mask torso
    for i in [8, 11]:
        pointx, pointy = pose_data[i]
        if pointx<1 and pointy<1:
            continue
        agnostic_draw.ellipse((pointx-r*3, pointy-r*6, pointx+r*3, pointy+r*6), 'black', 'black')

    line_points = []
    for i in [2, 8]:
        if pose_data[i][0]<1 and pose_data[i][1]<1:
            continue
        line_points.append(tuple(pose_data[i]))
    agnostic_draw.line(line_points, 'black', width=r*6)

    line_points = []
    for i in [5, 11]:
        if pose_data[i][0]<1 and pose_data[i][1]<1:
            continue
        line_points.append(tuple(pose_data[i]))
    agnostic_draw.line(line_points, 'black', width=r*6)

    line_points = []
    for i in [8, 11]:
        if pose_data[i][0]<1 and pose_data[i][1]<1:
            continue
        line_points.append(tuple(pose_data[i]))
    agnostic_draw.line(line_points, 'black', width=r*12)

    line_points = []
    for i in [2, 5, 11, 8]:
        if pose_data[i][0]<1 and pose_data[i][1]<1:
            continue
        line_points.append(tuple(pose_data[i]))

    if len(line_points)>1 and len(line_points[0])>1:
        agnostic_draw.polygon(line_points, 'black', 'black')

    # mask neck
    pointx, pointy = pose_data[1]
    agnostic_draw.rectangle((pointx-r*6, pointy-r*6, pointx+r*6, pointy+r*6), 'black', 'black')

    return agnostic

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, help="dataset dir")
    parser.add_argument('--output_path', type=str, help="output dir")

    args = parser.parse_args()
    data_path = args.data_path
    output_path = args.output_path
    
    os.makedirs(output_path, exist_ok=True)

    for im_name in tqdm(os.listdir(osp.join(data_path, 'images'))):
        if '_1.jpg' in im_name:
            continue

        img = Image.open(osp.join(data_path, 'images', im_name)).convert("RGB")

        json_name = im_name.replace('_0.jpg', '_2.json')
        with open(osp.join(data_path, 'keypoints', json_name)) as f:
            json_file = json.load(f)
            pose_data = json_file['keypoints']
            pose_data = np.array(pose_data)
            pose_data = pose_data[:, :2] * 2

        agnostic = get_img_agnostic_onlypose(img, pose_data)
        
        agnostic.save(osp.join(output_path, im_name))