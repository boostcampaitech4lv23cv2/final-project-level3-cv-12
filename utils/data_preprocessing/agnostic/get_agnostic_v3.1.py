import cv2
import os
from os import path as osp
from PIL import Image, ImageDraw
import numpy as np
from numpy.linalg import lstsq
import json

import torch
import torchvision.transforms as transforms
from torchvision import utils

from tqdm import tqdm
import argparse


label_map={
    "background": 0,
    "hat": 1,
    "hair": 2,
    "sunglasses": 3,
    "upper_clothes": 4,
    "skirt": 5,
    "pants": 6,
    "dress": 7,
    "belt": 8,
    "left_shoe": 9,
    "right_shoe": 10,
    "head": 11,
    "left_leg": 12,
    "right_leg": 13,
    "left_arm": 14,
    "right_arm": 15,
    "bag": 16,
    "scarf": 17,
}


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--data_path', type=str, default='../data/dress_code', help='dataset dir')
    parser.add_argument('--part', nargs='+', default=['upper_body'], help='어느 부위를 agnostic 이미지로 만들것인지 작성')

    parser.add_argument('--radius', type=int, default=10)
    parser.add_argument('--height', type=int, default=1024)
    parser.add_argument('--width', type=int, default=768)

    parser.add_argument('--add_parse_agnostic', action='store_true', help='parsing image를 기반으로 만든 agnostic을 추가로 저장함')

    args = parser.parse_args()
    return args


def get_agnostic(args, imgs, im_parse, pose_label, part):
    transform = transforms.Compose([
        transforms.ToTensor(),
        # transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    transform2D = transforms.Compose([
        transforms.ToTensor(),
        # transforms.Normalize((0.5, ), (0.5, ))
    ])
    img = transform(imgs)
    img_parse = im_parse
    parse_array = np.array(img_parse)
    pose_datas = pose_label


    parse_head = (parse_array == 1).astype(np.float32) + \
                 (parse_array == 2).astype(np.float32) + \
                 (parse_array == 3).astype(np.float32) + \
                 (parse_array == 11).astype(np.float32)

    parser_mask_fixed = (parse_array == label_map["hair"]).astype(np.float32) + \
                        (parse_array == label_map["left_shoe"]).astype(np.float32) + \
                        (parse_array == label_map["right_shoe"]).astype(np.float32) + \
                        (parse_array == label_map["hat"]).astype(np.float32) + \
                        (parse_array == label_map["sunglasses"]).astype(np.float32) + \
                        (parse_array == label_map["scarf"]).astype(np.float32) + \
                        (parse_array == label_map["bag"]).astype(np.float32)

    parser_mask_changeable = (parse_array == label_map["background"]).astype(np.float32)

    arms = (parse_array == 14).astype(np.float32) + (parse_array == 15).astype(np.float32)

    if part == 'dresses':
        label_cat = 7
        parse_mask = (parse_array == 7).astype(np.float32) + \
                     (parse_array == 12).astype(np.float32) + \
                     (parse_array == 13).astype(np.float32)

        parser_mask_changeable += np.logical_and(parse_array, np.logical_not(parser_mask_fixed))

    elif part == 'upper_body':
        label_cat = 4
        parse_mask = (parse_array == 4).astype(np.float32)

        parser_mask_fixed += (parse_array == label_map["skirt"]).astype(np.float32) + \
                             (parse_array == label_map["pants"]).astype(np.float32)
        parser_mask_changeable += np.logical_and(parse_array, np.logical_not(parser_mask_fixed))

    elif part == 'lower_body':
        label_cat = 6
        parse_mask = (parse_array == 6).astype(np.float32) + \
                     (parse_array == 12).astype(np.float32) + \
                     (parse_array == 13).astype(np.float32)

        parser_mask_fixed += (parse_array == label_map["upper_clothes"]).astype(np.float32) + \
                             (parse_array == 14).astype(np.float32) + \
                             (parse_array == 15).astype(np.float32)
        parser_mask_changeable += np.logical_and(parse_array, np.logical_not(parser_mask_fixed))

    parse_head = torch.from_numpy(parse_head)  # [0,1]
    parse_mask = torch.from_numpy(parse_mask)  # [0,1]
    parser_mask_fixed = torch.from_numpy(parser_mask_fixed)
    parser_mask_changeable = torch.from_numpy(parser_mask_changeable)

    # dilation
    parse_mask = parse_mask.cpu().numpy()

    # Load pose points
    pose_data = pose_datas['keypoints']
    pose_data = np.array(pose_data)
    pose_data = pose_data.reshape((-1, 4))


    point_num = pose_data.shape[0]
    r = args.radius * (args.height/512.0)
    im_pose = Image.new('L', (args.width, args.height))
    pose_draw = ImageDraw.Draw(im_pose)
    neck = Image.new('L', (args.width, args.height))
    neck_draw = ImageDraw.Draw(neck)

    for i in range(point_num):
        one_map = Image.new('L', (args.width, args.height))
        draw = ImageDraw.Draw(one_map)
        point_x = np.multiply(pose_data[i, 0], args.width/384.0)
        point_y = np.multiply(pose_data[i, 1], args.height/512.0)
        if point_x > 1 and point_y > 1:
            draw.rectangle((point_x - r, point_y - r, point_x + r, point_y + r), 'white', 'white')
            pose_draw.rectangle((point_x - r, point_y - r, point_x + r, point_y + r), 'white', 'white')
            if i == 2 or i == 5:
                neck_draw.ellipse((point_x - r*4, point_y - r*4, point_x + r*4, point_y + r*4), 'white', 'white')
        one_map = transform2D(one_map)

    im_arms = Image.new('L', (args.width, args.height))
    arms_draw = ImageDraw.Draw(im_arms)

    parse_head_2 = torch.clone(parse_head)
    if part == 'dresses' or part == 'upper_body':
        data = pose_datas
        shoulder_right = np.multiply(tuple(data['keypoints'][2][:2]), args.height / 512.0)
        shoulder_left = np.multiply(tuple(data['keypoints'][5][:2]), args.height / 512.0)
        elbow_right = np.multiply(tuple(data['keypoints'][3][:2]), args.height / 512.0)
        elbow_left = np.multiply(tuple(data['keypoints'][6][:2]), args.height / 512.0)
        wrist_right = np.multiply(tuple(data['keypoints'][4][:2]), args.height / 512.0)
        wrist_left = np.multiply(tuple(data['keypoints'][7][:2]), args.height / 512.0)

        if wrist_right[0] <= 1. and wrist_right[1] <= 1.:
            if elbow_right[0] <= 1. and elbow_right[1] <= 1.:
                arms_draw.line(np.concatenate((wrist_left, elbow_left, shoulder_left, shoulder_right)).astype(np.uint16).tolist(), 'white', 30, 'curve')
            else:
                arms_draw.line(np.concatenate((wrist_left, elbow_left, shoulder_left, shoulder_right, elbow_right)).astype(np.uint16).tolist(), 'white', 30, 'curve')

        elif wrist_left[0] <= 1. and wrist_left[1] <= 1.:
            if elbow_left[0] <= 1. and elbow_left[1] <= 1.:
                arms_draw.line(np.concatenate((shoulder_left, shoulder_right, elbow_right, wrist_right)).astype(np.uint16).tolist(), 'white', 30, 'curve')
            else:
                arms_draw.line(np.concatenate((elbow_left, shoulder_left, shoulder_right, elbow_right, wrist_right)).astype(np.uint16).tolist(), 'white', 30, 'curve')

        else:
            arms_draw.line(np.concatenate((wrist_left, elbow_left, shoulder_left, shoulder_right, elbow_right, wrist_right)).astype(np.uint16).tolist(),'white', 30, 'curve')

        if args.height > 512:
            im_arms = cv2.dilate(np.float32(im_arms), np.ones((10, 10), np.uint16), iterations=5)
        # elif args.height > 256:
        #     im_arms = cv2.dilate(np.float32(im_arms), np.ones((5, 5), np.uint16), iterations=5)
        hands = np.logical_and(np.logical_not(im_arms), arms)
        parse_mask += im_arms
        parser_mask_fixed += hands

        points = []
        points.append(np.multiply(tuple(data['keypoints'][2][:2]), args.height/512.0))
        points.append(np.multiply(tuple(data['keypoints'][5][:2]), args.height/512.0))
        x_coords, y_coords = zip(*points)
        A = np.vstack([x_coords, np.ones(len(x_coords))]).T
        m, c = lstsq(A, y_coords, rcond=None)[0]
        for i in range(parse_array.shape[1]):
            y = i * m + c
            parse_head_2[int(y - 20*(args.height/512.0)):, i] = 0

    parser_mask_fixed = np.logical_or(parser_mask_fixed, np.array(parse_head_2, dtype=np.uint16))
    parse_mask += np.logical_or(parse_mask, np.logical_and(np.array(parse_head, dtype=np.uint16), np.logical_not(np.array(parse_head_2, dtype=np.uint16))))

    if args.height > 512:
        parse_mask = cv2.dilate(parse_mask, np.ones((20, 20), np.uint16), iterations=5)
    else:
        parse_mask = cv2.dilate(parse_mask, np.ones((5, 5), np.uint16), iterations=5)

    parse_mask = np.logical_and(parser_mask_changeable, np.logical_not(parse_mask))
    parse_mask_total = np.logical_or(parse_mask, parser_mask_fixed)
    
    im_mask = img * parse_mask_total
    if args.add_parse_agnostic:
        img_parse_transform = transforms.Compose([
            transforms.ToTensor()
        ])
        parse_mask = img_parse_transform(img_parse) * parse_mask_total
        return im_mask, parse_mask
    return im_mask


if __name__ == "__main__":
    args = get_args()

    for p in args.part:
        os.makedirs(os.path.join(args.data_path, p, 'agnostic'), exist_ok=True)
        if args.add_parse_agnostic:
            os.makedirs(os.path.join(args.data_path, p, 'parse_agnostic'), exist_ok=True)

        for im_name in tqdm(os.listdir(osp.join(args.data_path, p, 'images'))):
            if '_1.jpg' in im_name:
                continue
            
            # human image
            imgs = Image.open(osp.join(args.data_path, p, 'images', im_name)).convert('RGB')
            
            # human parse image
            parse_name = im_name.replace('_0.jpg', '_4.png')
            im_parse = Image.open(osp.join(args.data_path, p, 'label_maps', parse_name))

            # pose label data
            pose_name = im_name.replace('_0.jpg', '_2.json')
            with open(osp.join(args.data_path, p, 'keypoints', pose_name), 'r') as f:
                pose_label = json.load(f)

            if args.add_parse_agnostic:
                agnostic_img, parse_mask = get_agnostic(args, imgs, im_parse, pose_label, p)
                utils.save_image(agnostic_img, osp.join(args.data_path, p, 'agnostic', im_name))
                utils.save_image(parse_mask, osp.join(args.data_path, p, 'parse_agnostic', im_name))

            else:
                agnostic_img = get_agnostic(args, imgs, im_parse, pose_label, p)
                utils.save_image(agnostic_img, osp.join(args.data_path, p, 'agnostic', im_name))