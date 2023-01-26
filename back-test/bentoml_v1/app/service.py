import torch
from model import SDAFNet_Tryon, get_model, get_avatar, _transform_image
import bentoml
from PIL import Image
import torch.backends.cudnn as cudnn
from bentoml.io import Image
import numpy as np
from torchvision import transforms

cudnn.benchmark = True
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

vton_model = bentoml.models.get('model_daflow:latest')
vton_runner = vton_model.to_runner()

svc = bentoml.Service('vton_daflow', runners=[vton_runner])

@svc.api(input=Image(), output=Image())
async def predict_from_image_byte(image):
    model = bentoml.pytorch.load_model("model_daflow:latest").to(device)
    
    image = np.array(image)
    transformed_image = _transform_image(image).to(device)
    result = get_avatar()
    img = result['img'].to(device)
    img_agnostic = result['agnostic'].to(device) #Masked model image
    img_agnostic = img_agnostic.unsqueeze(0)
    pose = result['pose'].to(device)
    pose = pose.unsqueeze(0)
    cloth_img = transformed_image.to(device)

    ref_input = torch.cat((pose, img_agnostic), dim=1)

    tryon_result = model(ref_input, cloth_img, img_agnostic).detach()

    transf = transforms.ToPILImage()
    imgs = transf(tryon_result.squeeze())

    return imgs