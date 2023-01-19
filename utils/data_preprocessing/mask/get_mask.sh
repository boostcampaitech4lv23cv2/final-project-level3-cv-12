#!/bin/bash

PATH_MAIN="Enter root dir" #"/opt/ml/lv3/data/dress_code/mix/upper_body"

# 1. Make Folders
mkdir $PATH_MAIN/temp_image_cloth
mkdir $PATH_MAIN/temp_image_cloth_rmbkg
mkdir $PATH_MAIN/cloth_mask


# 2. [carvekit] make background_removed image from original image
echo Move cloth images to temp_dir
mv $PATH_MAIN/images/*_1.jpg $PATH_MAIN/temp_image_cloth

carvekit -i $PATH_MAIN/temp_image_cloth -o $PATH_MAIN/temp_image_cloth_rmbkg --device cuda

echo Move cloth images to original_dir
mv $PATH_MAIN/temp_image_cloth/*.jpg $PATH_MAIN/images/


# 3. [get_mask.py] generate mask image from background_removed image
python3 /opt/ml/final-project-level3-cv-12/utils/data_preprocessing/mask/get_mask.py --PATH_IN $PATH_MAIN/temp_image_cloth_rmbkg --PATH_OUT $PATH_MAIN/cloth_mask --PATH_ID $PATH_MAIN/images