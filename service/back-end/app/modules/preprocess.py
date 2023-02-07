from modules.openpose.openpose import Openpose
import cv2
import numpy as np
from modules.human_parser.simple_extractor import get_parser_map
from modules.agnostic.get_agnostic import get_agnostic
from torchvision import transforms


def cloth_removed_background(interface, image):
    images_without_background = interface([image])
    cat_wo_bg = np.array(images_without_background[0])

    image = cat_wo_bg[:, :, :3]
    mask0 = cat_wo_bg[:, :, 3] < 230

    image[mask0] = np.array([255, 255, 255])

    image = np.array(image)

    return image


def get_openpose(model, human):
    openpose = Openpose(model)
    human_bgr = cv2.cvtColor(human, cv2.COLOR_RGB2BGR)
    openpose_result = openpose.get_bodypose(human_bgr)

    return openpose_result  # skeleton은 image, keypoint는 json


def get_human_parse(model, human):
    parser_map = get_parser_map(model, human)

    return parser_map


def get_human_agnostic(human, human_parse, keypoint, part):
    h, w, _ = np.array(human).shape
    radius = 10
    human_np = np.array(human)
    agnostic = get_agnostic(human_np, human_parse, keypoint, part, h, w, radius)

    return agnostic


def transform_image(image):
    image = transforms.Resize((512, 384), interpolation=2)(image)
    image = transforms.ToTensor()(image)
    image = transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))(image)

    return image
