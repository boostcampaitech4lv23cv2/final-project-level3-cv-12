import bentoml
import argparse
import torch
import os

from modules.model import get_model

from modules.openpose.model import bodypose_model
from modules.openpose.util import transfer

from carvekit.ml.wrap.tracer_b7 import TracerUniversalB7
from carvekit.ml.wrap.fba_matting import FBAMatting

from modules.human_parser import networks
from collections import OrderedDict

def get_config():
    dir_root = os.getcwd()
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--daflow-path', default=os.path.join(dir_root, 'service/back-end/checkpoints/daflow/100_mod_all_256.pt'), help='saved daflow model path') # 025_model_lower_512_2_lr00003
    parser.add_argument('--openpose-path', default=os.path.join(dir_root, 'service/back-end/checkpoints/openpose/body_pose_model.pth'), help='saved openpose model path')
    parser.add_argument('--parser-path', default=os.path.join(dir_root, 'service/back-end/checkpoints/human_parser/exp-schp-201908301523-atr.pth'), help='saved human parser model path')
    parser.add_argument('--device', default='cuda' if torch.cuda.is_available() else 'cpu', help='check device')
    parser.add_argument('--batch-size-matting', default=1, type=int)
    parser.add_argument('--batch-size-seg', default=1, type=int)
    parser.add_argument('--matting-mask-size', default=2048, type=int)
    parser.add_argument('--seg-mask-size', default=640, type=int)
    parser.add_argument('--fp16', action='store_true')
    parser.add_argument('--parser-classes', default=18, type=int)
    config = parser.parse_args()
    
    return config

if __name__ == "__main__":
    config = get_config()
    
    ## Virtual try-on
    daflow = get_model(model_path=config.daflow_path)
    
    bentoml.pytorch.save_model('daflow', daflow)
    print('save daflow done.')
    
    ## models for cloth without background
    fba = FBAMatting(
        batch_size=config.batch_size_matting,
        device=config.device,
        input_tensor_size=config.matting_mask_size,
        fp16=config.fp16,
    ).to(config.device).eval()
    
    bentoml.pytorch.save_model('fbamatting', fba)
    print('save fbamatting done.')
    
    tracer = TracerUniversalB7(
        device=config.device,
        batch_size=config.batch_size_seg,
        input_image_size=config.seg_mask_size,
        fp16=config.fp16,
    ).to(config.device).eval()
    
    bentoml.pytorch.save_model('traceruniversal', tracer)
    print('save traceruniversal done.')
    
    ## openpose
    openpose = bodypose_model().to(config.device)
    model_dict = transfer(openpose, torch.load(config.openpose_path))
    openpose.load_state_dict(model_dict)
    openpose.eval()
    
    bentoml.pytorch.save_model('openpose', openpose)
    print('save openpose done.')
    
    ## human parser
    human_parser = networks.init_model('resnet101', num_classes=config.parser_classes, pretrained=None).to(config.device)
    state_dict = torch.load(config.parser_path)['state_dict']
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = k[7:]  # remove `module.`
        new_state_dict[name] = v
    human_parser.load_state_dict(new_state_dict)
    human_parser.eval()
    
    bentoml.pytorch.save_model('human_parser', human_parser)
    print('save human_parser done.')