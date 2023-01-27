from model import get_model
import bentoml
import argparse
import torch
from openpose.model import bodypose_model
from openpose.util import transfer
from model import SDAFNet_Tryon

def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model-path', default='/opt/ml/input/038_model_all_256_part2.pt', help='saved model path')
    parser.add_argument('--openpose_path', default='./model/body_pose_model.pth', help='saved openpose model path')

    config = parser.parse_args()
    
    return config

if __name__ == "__main__":
    config = get_config()
    sdafnet = SDAFNet_Tryon(ref_in_channel=6)
    model = get_model(model_path=config.model_path)
    bentoml.pytorch.save_model('model_daflow', model)
    openpose_model = bodypose_model()
    model_dict = transfer(openpose_model,torch.load(config.openpose_path))
    openpose_model.load_state_dict(model_dict)
    openpose_model.eval()
    bentoml.pytorch.save_model('model_openpose', openpose_model)
