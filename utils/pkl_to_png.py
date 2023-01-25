from argparse import ArgumentParser
import numpy as np
import torch
import cv2
import os

densepose_cmap = np.array([
    [0, 0, 0], #background
	[105, 105, 105], # ? 회색
	[85, 107, 47], # body
	[139, 69, 19], # hand right
	[72, 61, 139], # hand left
	[0, 128, 0], # foot left
	[154, 205, 50], # foot right
	[0, 0, 139], 
	[255, 69, 0],
	[255, 165, 0], # upper leg right
	[255, 255, 0], # upper leg left
	[0, 255, 0],
	[186, 85, 211],
	[0, 255, 127], # lower leg right
	[220, 20, 60], # lower leg left
	[0, 191, 255], # upper arm left 몸쪽
	[0, 0, 255], #upper arm right 몸쪽
	[216, 191, 216], # upper arm left 바깥쪽
	[255, 0, 255], # upper arm right 바깥
	[30, 144, 255], # lower arm left 몸쪽
	[219, 112, 147], # lower arm right 몸쪽
	[240, 230, 140], # lower arm left 바깥쪽
	[255, 20, 147], # lower arm right 바깥쪽
	[255, 160, 122], # head right
	[127, 255, 212] # head left
])

# rgb to bgr
for i in densepose_cmap:
    tmp = i[0]
    i[0] = i[2]
    i[2] = tmp

def parse_args():
    parser = ArgumentParser()

    parser.add_argument('--pkl_path', type=str, default='/opt/ml/input/SplitData/upper_body/upper_body.pkl')
    parser.add_argument('--output_dir', type=str, default='/opt/ml/input/SplitData/upper_body/CVTON_densepose')

    args = parser.parse_args()

    return args

def pkl_to_png(args):
    with open(args.pkl_path, "rb") as f:
        dp_frame = torch.load(f)
    if isinstance(dp_frame, dict):
        dp_frame = [dp_frame]
    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)
    for i, image in enumerate(dp_frame):
        assert len(image['scores']) != 0, f'{args.pkl_path} does not contain persons'
        print(f"processing {image['file_name']}")
        raw_image = cv2.imread(image['file_name'])
        seg_image = np.zeros(raw_image.shape, np.uint8)
        bbox_xywh = image['pred_boxes_XYXY'].clone()
        bbox_xywh[:, 2] -= bbox_xywh[:, 0]
        bbox_xywh[:, 3] -= bbox_xywh[:, 1]
        
        for j, result in enumerate(image['pred_densepose']):
            result = image['pred_densepose'][0]
            x, y, w, h = [int(v) for v in bbox_xywh[0]]
            matrix = result.labels.cpu().numpy()

            # matrix = iuv_array[0,:,:].cpu().numpy()
            segm = matrix[:,:]
            mask = np.zeros(matrix.shape, dtype=np.uint8)
            mask[segm > 0] = 1
            matrix = densepose_cmap[matrix]
            mask = cv2.resize(mask, (w, h), cv2.INTER_NEAREST)
            matrix = cv2.resize(matrix.astype(np.uint8), (w, h), cv2.INTER_NEAREST)
            mask_bg = np.tile((mask == 0)[:, :, np.newaxis], [1, 1, 3])
            matrix[mask_bg] = seg_image[y : y + h, x : x + w, :][mask_bg]
            seg_image[y : y + h, x : x + w, :] = matrix

        cv2.imwrite(os.path.join(args.output_dir, os.path.basename(f"{image['file_name']}")), seg_image)
    return

if __name__ == "__main__":
    args = parse_args()
    pkl_to_png(args)
    