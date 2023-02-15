import torch
from modules.model import get_avatar, _transform_image
import modules.preprocess as preprocess
import bentoml
from PIL import Image as pImage
import torch.backends.cudnn as cudnn
from bentoml.io import Image, Multipart, Text
import numpy as np
from torchvision import transforms
from modules.carvekit_custom.high import HiInterface
import cv2

from concurrent.futures import ThreadPoolExecutor

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

    tryon_result = ((tryon_result.squeeze().permute(1, 2, 0).cpu().numpy()*0.5+0.5)*255).astype(np.uint8)
    tryon_result = transforms.ToPILImage()(tryon_result)

    return tryon_result

@svc.api(input=Multipart(part=Text(), cloth=Image(), human=Image()), output=Image(), route='/all-tryon')
def predict_from_cloth_human(part, cloth, human):
    human = np.array(human)

    with ThreadPoolExecutor(3) as executor:
        openpose = executor.submit(preprocess.get_openpose, openpose_runner, human)
        cloth = executor.submit(preprocess.cloth_removed_background, interface, cloth)
        parser_map = executor.submit(preprocess.get_human_parse, parser_runner, human)
    
    skeleton, keypoint = openpose.result()
    cloth = cloth.result()
    parser_map = parser_map.result()
    
    cloth_img = _transform_image(cloth).to(device)

    img_agnostic = preprocess.get_human_agnostic(human, parser_map, keypoint, part)
    img_agnostic = (img_agnostic.permute(1, 2, 0).numpy()*255).astype(np.uint8)
    img_agnostic = preprocess.transform_image(pImage.fromarray(img_agnostic))
    img_agnostic = img_agnostic.to(device) # Masked model image
    img_agnostic = img_agnostic.unsqueeze(0)
    
    skeleton = skeleton.astype(np.uint8)
    skeleton = cv2.cvtColor(skeleton, cv2.COLOR_BGR2RGB)
    skeleton = preprocess.transform_image(pImage.fromarray(skeleton))
    skeleton = skeleton.to(device)
    skeleton = skeleton.unsqueeze(0)

    ref_input = torch.cat((skeleton, img_agnostic), dim=1)
        
    tryon_result = vton_runner.run(ref_input, cloth_img, img_agnostic).detach()

    tryon_result = ((tryon_result.squeeze().permute(1, 2, 0).cpu().numpy()*0.5+0.5)*255).astype(np.uint8)
    tryon_result = transforms.ToPILImage()(tryon_result)
        
    return tryon_result