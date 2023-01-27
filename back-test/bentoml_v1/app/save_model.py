from model import get_model
import bentoml
import argparse
from carvekit.ml.wrap.tracer_b7 import TracerUniversalB7
from carvekit.ml.wrap.fba_matting import FBAMatting
import torch

def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--daflow-path', default='/opt/ml/input/038_model_all_256_part2.pt', help='saved daflow-model path')
    parser.add_argument('--device', default='cuda' if torch.cuda.is_available() else 'cpu', help='check device')
    parser.add_argument('--batch_size_matting', default=1, type=int)
    parser.add_argument('--batch_size_seg', default=1, type=int)
    parser.add_argument('--matting-mask-size', default=2048, type=int)
    parser.add_argument('--seg-mask-size', default=640, type=int)
    parser.add_argument('--fp16', action='store_true')
    config = parser.parse_args()
    
    return config

if __name__ == "__main__":
    config = get_config()
    
    ## Virtual try-on
    daflow = get_model(model_path=config.daflow_path)
    bentoml.pytorch.save_model('daflow', daflow)
    
    ## models for cloth without background
    fba = FBAMatting(
        batch_size=config.batch_size_matting,
        device=config.device,
        input_tensor_size=config.matting_mask_size,
        fp16=config.fp16,
    )
    bentoml.pytorch.save_model('fbamatting', fba)
    
    tracer = TracerUniversalB7(
        device=config.device,
        batch_size=config.batch_size_seg,
        input_image_size=config.seg_mask_size,
        fp16=config.fp16,
    )
    bentoml.pytorch.save_model('traceruniversal', tracer)