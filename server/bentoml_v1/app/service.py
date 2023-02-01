import torch
from model import get_avatar, _transform_image
import preprocess 
import bentoml
from PIL import Image as pImage
import torch.backends.cudnn as cudnn
from bentoml.io import Image, Multipart, Text
import numpy as np
from torchvision import transforms
from carvekit_custom.high import HiInterface
import os
import json

from torchvision.utils import save_image

cudnn.benchmark = True
device = 'cuda' if torch.cuda.is_available() else 'cpu'

vton_model = bentoml.models.get('daflow:latest')
vton_runner = vton_model.to_runner()

openpose_model = bentoml.models.get('openpose:latest')
openpose_runner = openpose_model.to_runner()

tracer_model = bentoml.models.get('traceruniversal:latest')
tracer_runner = tracer_model.to_runner()

fba_model = bentoml.models.get('fbamatting:latest')
fba_runner = fba_model.to_runner()

parser_model = bentoml.models.get('human_parser:latest')
parser_runner = parser_model.to_runner()

svc = bentoml.Service('vton_daflow', runners=[vton_runner, openpose_runner, tracer_runner, fba_runner, parser_runner])

interface = HiInterface(object_type="object",  # Can be "object" or "hairs-like".
                            batch_size_seg=1,
                            device=device,
                            seg_mask_size=640,  # Use 640 for Tracer B7 and 320 for U2Net
                            trimap_prob_threshold=231,
                            trimap_dilation=30,
                            trimap_erosion_iters=5,
                            fp16=False,
                            fba=fba_runner,
                            tracer=tracer_runner)

@svc.api(input=Multipart(cloth=Image(), avatar_path=Text()), output=Image(), route='/cloth-tryon')
async def predict_from_cloth(cloth, avatar_path):
    image = preprocess.cloth_removed_background(interface, cloth)
    cloth_img = _transform_image(image).to(device)
    
    # need avatar_id && avatar_dir_path
    result = get_avatar(avatar_path=avatar_path)

    img_agnostic = result['agnostic'].to(device) #Masked model image
    img_agnostic = img_agnostic.unsqueeze(0)

    pose = result['pose'].to(device)
    pose = pose.unsqueeze(0)

    ref_input = torch.cat((pose, img_agnostic), dim=1)

    tryon_result = vton_runner.run(ref_input, cloth_img, img_agnostic).detach()

    save_image(tryon_result, '/opt/ml/final/result.jpg', nrow=1, normalize=True, range=(-1,1))

    imgs = ((tryon_result.squeeze().permute(1, 2, 0).cpu().numpy()*0.5+0.5)*255).astype(np.uint8)
    transf = transforms.ToPILImage()
    imgs = transf(imgs)

    return imgs

save_dir = '/opt/ml/input/final-project-level3-cv-12/server/bentoml_v1/app/result_sample'
os.makedirs(save_dir, exist_ok=True)

@svc.api(input=Multipart(part=Text(), cloth=Image(), human=Image()), output=Image(), route='/all-tryon')
async def predict_from_cloth_human(part, cloth, human):
    cloth = preprocess.cloth_removed_background(interface, cloth)
    cloth_img = _transform_image(cloth).to(device)
    test = ((cloth_img.squeeze().permute(1, 2, 0).cpu().numpy()*0.5+0.5)*255).astype(np.uint8)
    pImage.fromarray(test).save(f'{save_dir}/cloth.png', 'png')

    skeleton, keypoint = preprocess.get_openpose(openpose_runner, human)
    parser_map = preprocess.get_human_parse(parser_runner, human)
    parser_map.save(f'{save_dir}/parser_map.png', 'png')

    print(keypoint)
    with open(f'{save_dir}/keypoints.json', 'w') as f:
        json.dump(keypoint, f)
    
    img_agnostic = preprocess.get_human_agnostic(human, parser_map, keypoint, part)
    img_agnostic = (img_agnostic.permute(1, 2, 0).numpy()*255).astype(np.uint8)
    
    pImage.fromarray(img_agnostic).save(f'{save_dir}/agnostic.png', 'png')
    img_agnostic = preprocess.transform_image(pImage.fromarray(img_agnostic))
    img_agnostic = img_agnostic.to(device) # Masked model image
    img_agnostic = img_agnostic.unsqueeze(0)
    
    skeleton = (skeleton*255).astype(np.uint8)
    pImage.fromarray(skeleton).save(f'{save_dir}/skeleton.png', 'png')
    skeleton = preprocess.transform_image(pImage.fromarray(skeleton))
    skeleton = skeleton.to(device)
    skeleton = skeleton.unsqueeze(0)

    ref_input = torch.cat((skeleton, img_agnostic), dim=1)
        
    tryon_result = vton_runner.run(ref_input, cloth_img, img_agnostic).detach()

    imgs = ((tryon_result.squeeze().permute(1, 2, 0).cpu().numpy()*0.5+0.5)*255).astype(np.uint8)
    transf = transforms.ToPILImage()
    imgs = transf(imgs)
    
    imgs.save(f'{save_dir}/result.png', 'png')
    
    return imgs