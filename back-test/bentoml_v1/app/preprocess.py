from openpose.model import bodypose_model
from openpose.util import transfer
from openpose.body import Body
from openpose.openpose import Openpose

import bentoml
import cv2
import numpy as np
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_openpose(human):
    openpose_model = bentoml.pytorch.load_model("model_openpose:latest").to(device)
    openpose = Openpose(openpose_model)
    numpy_image=np.array(human)  
    human_bgr=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
    skeleton, keypoint = openpose.get_bodypose(human_bgr)
    return skeleton, keypoint   # skeleton은 image, keypoint는 json