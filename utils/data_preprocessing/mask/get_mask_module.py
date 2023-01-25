import torch
from carvekit.api.high import HiInterface
import numpy as np

def get_white_bg(path_image, threshold_pixval=230, save_name=''):
    # Check carvekit.api.high.HiInterface for more information
    interface = HiInterface(object_type="object",  # Can be "object" or "hairs-like".
                            batch_size_seg=1,
                            batch_size_matting=1,
                            device='cuda' if torch.cuda.is_available() else 'cpu',
                            seg_mask_size=640,  # Use 640 for Tracer B7 and 320 for U2Net
                            matting_mask_size=2048,
                            trimap_prob_threshold=231,
                            trimap_dilation=30,
                            trimap_erosion_iters=5,
                            fp16=False)
    images_without_background = interface([path_image])
    cat_wo_bg = np.array(images_without_background[0])

    image = cat_wo_bg[:, :, :3]

    mask0 = cat_wo_bg[:, :, 3] < threshold_pixval

    image[mask0] = np.array([255, 255, 255])

    if save_name:
        print('save_name')
        from PIL import Image
        mask = Image.fromarray(image)
        mask.save(save_name + '.png')
    
    return image


def get_binary_mask(path_image, threshold_pixval=230, save_name=''):
    # Check carvekit.api.high.HiInterface for more information
    interface = HiInterface(object_type="object",  # Can be "object" or "hairs-like".
                            batch_size_seg=1,
                            batch_size_matting=1,
                            device='cuda' if torch.cuda.is_available() else 'cpu',
                            seg_mask_size=640,  # Use 640 for Tracer B7 and 320 for U2Net
                            matting_mask_size=2048,
                            trimap_prob_threshold=231,
                            trimap_dilation=30,
                            trimap_erosion_iters=5,
                            fp16=False)
    images_without_background = interface([path_image])
    cat_wo_bg = images_without_background[0]
    
    mask = np.array(cat_wo_bg)[:, :, 3]

    mask0 = mask < threshold_pixval
    mask[mask0] = 0
    mask[np.logical_not(mask0)] = 255

    if save_name:
        from PIL import Image
        mask = Image.fromarray(mask)
        mask.save(save_name + '.png')
    
    return mask