import cv2
from PIL import Image, ImageDraw
import numpy as np
from numpy.linalg import lstsq

import torch
import torchvision.transforms as transforms

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

def get_agnostic(imgs, im_parse, pose_label, part, height, width, radius):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    transform2D = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, ), (0.5, ))
    ])
    img = transform(imgs)
    img_parse = im_parse
    parse_array = np.array(img_parse)
    pose_datas = pose_label


    parse_head = (parse_array == 1).astype(np.float32) + \
                 (parse_array == 2).astype(np.float32) + \
                 (parse_array == 3).astype(np.float32) + \
                 (parse_array == 11).astype(np.float32)
    
    parse_mask = np.zeros((1))

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
    r = radius * (height/512.0)
    im_pose = Image.new('L', (width, height))
    pose_draw = ImageDraw.Draw(im_pose)
    neck = Image.new('L', (width, height))
    neck_draw = ImageDraw.Draw(neck)

    for i in range(point_num):
        one_map = Image.new('L', (width, height))
        draw = ImageDraw.Draw(one_map)
        point_x = np.multiply(pose_data[i, 0], width/384.0)
        point_y = np.multiply(pose_data[i, 1], height/512.0)
        if point_x > 1 and point_y > 1:
            draw.rectangle((point_x - r, point_y - r, point_x + r, point_y + r), 'white', 'white')
            pose_draw.rectangle((point_x - r, point_y - r, point_x + r, point_y + r), 'white', 'white')
            if i == 2 or i == 5:
                neck_draw.ellipse((point_x - r*4, point_y - r*4, point_x + r*4, point_y + r*4), 'white', 'white')
        one_map = transform2D(one_map)

    im_arms = Image.new('L', (width, height))
    arms_draw = ImageDraw.Draw(im_arms)

    parse_head_2 = torch.clone(parse_head)
    if part == 'dresses' or part == 'upper_body':
        data = pose_datas
        shoulder_right = np.multiply(tuple(data['keypoints'][2][:2]), height / 512.0)
        shoulder_left = np.multiply(tuple(data['keypoints'][5][:2]), height / 512.0)
        elbow_right = np.multiply(tuple(data['keypoints'][3][:2]), height / 512.0)
        elbow_left = np.multiply(tuple(data['keypoints'][6][:2]), height / 512.0)
        wrist_right = np.multiply(tuple(data['keypoints'][4][:2]), height / 512.0)
        wrist_left = np.multiply(tuple(data['keypoints'][7][:2]), height / 512.0)

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

        if height > 512:
            im_arms = cv2.dilate(np.float32(im_arms), np.ones((10, 10), np.uint16), iterations=5)
        # elif height > 256:
        #     im_arms = cv2.dilate(np.float32(im_arms), np.ones((5, 5), np.uint16), iterations=5)
        hands = np.logical_and(np.logical_not(im_arms), arms)
        parse_mask += im_arms
        parser_mask_fixed += hands

        points = []
        points.append(np.multiply(tuple(data['keypoints'][2][:2]), height/512.0))
        points.append(np.multiply(tuple(data['keypoints'][5][:2]), height/512.0))
        x_coords, y_coords = zip(*points)
        A = np.vstack([x_coords, np.ones(len(x_coords))]).T
        m, c = lstsq(A, y_coords, rcond=None)[0]
        for i in range(parse_array.shape[1]):
            y = i * m + c
            parse_head_2[int(y - 20*(height/512.0)):, i] = 0

    parser_mask_fixed = np.logical_or(parser_mask_fixed, np.array(parse_head_2, dtype=np.uint16))
    parse_mask += np.logical_or(parse_mask, np.logical_and(np.array(parse_head, dtype=np.uint16), np.logical_not(np.array(parse_head_2, dtype=np.uint16))))

    if height > 512:
        parse_mask = cv2.dilate(parse_mask, np.ones((20, 20), np.uint16), iterations=5)
    else:
        parse_mask = cv2.dilate(parse_mask, np.ones((5, 5), np.uint16), iterations=5)

    parse_mask = np.logical_and(parser_mask_changeable, np.logical_not(parse_mask))
    parse_mask_total = np.logical_or(parse_mask, parser_mask_fixed)
    
    im_mask = img * parse_mask_total

    return im_mask