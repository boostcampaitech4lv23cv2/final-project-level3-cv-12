import torch
from model import get_avatar, _transform_image
import bentoml
from PIL import Image as pImage
import torch.backends.cudnn as cudnn
from bentoml.io import Image
import numpy as np
from torchvision import transforms
from carvekit.api.high import HiInterface

cudnn.benchmark = True
device = 'cuda' if torch.cuda.is_available() else 'cpu'

vton_model = bentoml.models.get('daflow:latest')
vton_runner = vton_model.to_runner()

tracer_model = bentoml.models.get('traceruniversal:latest')
tracer_runner = tracer_model.to_runner()

fba_model = bentoml.models.get('fbamatting:latest')
fba_runner = fba_model.to_runner()

svc = bentoml.Service('vton_daflow', runners=[vton_runner, tracer_runner, fba_runner])

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

@svc.api(input=Image(), output=Image())
async def predict_from_image_byte(image):
    images_without_background = interface([image])
    cat_wo_bg = np.array(images_without_background[0])

    image = cat_wo_bg[:, :, :3]
    mask0 = cat_wo_bg[:, :, 3] < 230

    image[mask0] = np.array([255, 255, 255])
    
    save_image = pImage.fromarray(image)
    save_image.save(f'/opt/ml/input/final-project-level3-cv-12/back-test/bentoml_v1/app/sample.png', 'png')

    transformed_image = _transform_image(image).to(device)
    cloth_img = transformed_image.to(device)
    
    result = get_avatar()

    img_agnostic = result['agnostic'].to(device) #Masked model image
    img_agnostic = img_agnostic.unsqueeze(0)

    pose = result['pose'].to(device)
    pose = pose.unsqueeze(0)

    ref_input = torch.cat((pose, img_agnostic), dim=1)

    tryon_result = vton_runner.run(ref_input, cloth_img, img_agnostic).detach()

    transf = transforms.ToPILImage()
    imgs = transf(tryon_result.squeeze())
    
    imgs.save(f'/opt/ml/input/final-project-level3-cv-12/back-test/bentoml_v1/app/result.png', 'png')

    return imgs