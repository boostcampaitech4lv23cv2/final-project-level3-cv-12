import os
import shutil
import glob
from tqdm import tqdm
import random
import numpy as np
import torch
import argparse

def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--split-num', default=5000, help='dataset split num')
    parser.add_argument('-d', '--data-root-path', default='/opt/ml/input/datasets', help='input data root path')
    parser.add_argument('-o', '--output-path', default='/opt/ml/input/split_datasets', help='output dir path')
    parser.add_argument('-s', '--seed', default=21, type=int, help='random seed')
    parser.add_argument('-m', '--mode', default='copy', help='select mode "copy" or "move"')
    config = parser.parse_args()
    
    return config

def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = False
    torch.backends.cudnn.benchmark = True

def split_dataset(config):    
    categories = ['upper_body', 'lower_body', 'dresses']
    sub_dirs = ['keypoints', 'label_maps', 'skeletons', 'dense', 'images']
    
    ## train_pairs.txt
    train_pairs_name = 'train_pairs.txt'
    ## test_pairs_name
    test_pairs_name = 'test_pairs_paired.txt'
    test_file_paths = []
    ## test_unpairs_name
    test_unpairs_name = 'test_pairs_unpaired.txt'
    
    ## make output dirs
    for categorie in categories:
        for sub_dir in sub_dirs:
            os.makedirs(os.path.join(config.output_path, categorie, sub_dir), exist_ok=True)

    ## move train files source dir to output dir
    for categorie in categories:
        for sub_dir in tqdm(sub_dirs):
            file_paths = sorted(glob.glob(os.path.join(config.data_root_path, categorie, sub_dir, '*')))

            if len(file_paths) > config.split_num:
                split_num = config.split_num
                
                if sub_dir == 'dense' or sub_dir == 'images':
                    split_num = config.split_num*2
                    
                file_paths, test_file_paths = file_paths[:split_num], file_paths[split_num:]
            
            if sub_dir == 'dense' or sub_dir == 'images':
                for i in tqdm(range(0, len(file_paths), 2)):
                    npzOrHuman_path = file_paths[i]
                    pngOrCloth_path = file_paths[i + 1]
                    
                    npzOrHuman_name = npzOrHuman_path.split('/')[-1]
                    pngOrCloth_name = pngOrCloth_path.split('/')[-1]
                    
                    if config.mode == 'copy':
                        shutil.copy2(npzOrHuman_path, os.path.join(config.output_path, categorie, sub_dir, npzOrHuman_name))
                        shutil.copy2(pngOrCloth_path, os.path.join(config.output_path, categorie, sub_dir, pngOrCloth_name))
                    elif config.mode == 'move':
                        shutil.move(npzOrHuman_path, os.path.join(config.output_path, categorie, sub_dir, npzOrHuman_name))
                        shutil.move(pngOrCloth_path, os.path.join(config.output_path, categorie, sub_dir, pngOrCloth_name))

                    if sub_dir == 'images':
                        train_pairs_path = os.path.join(config.output_path, categorie, train_pairs_name)
                        if os.path.exists(train_pairs_path):
                            with open(train_pairs_path, 'a') as file:
                                file.write(npzOrHuman_name + '\t' + pngOrCloth_name + '\n')
                        else:
                            with open(train_pairs_path, 'w') as file:
                                file.write(npzOrHuman_name + '\t' + pngOrCloth_name + '\n')
            else:
                for file_path in tqdm(file_paths):
                    file_name = file_path.split('/')[-1]
                    
                    if config.mode == 'copy':
                        shutil.copy2(file_path, os.path.join(config.output_path, categorie, sub_dir, file_name))
                    elif config.mode == 'move':
                        shutil.move(file_path, os.path.join(config.output_path, categorie, sub_dir, file_name))
    
    ## make test_pairs.txt
    test_cloth_paths = []
    for categorie in categories:
        test_pairs_path = os.path.join(config.output_path, categorie, test_pairs_name)
        
        for i in tqdm(range(0, len(test_file_paths), 2)):
            human_path = test_file_paths[i]
            cloth_path = test_file_paths[i + 1]
            test_cloth_paths.append(cloth_path)
            
            human_name = human_path.split('/')[-1]
            cloth_name = cloth_path.split('/')[-1]
            
            if os.path.exists(test_pairs_path):
                with open(test_pairs_path, 'a') as file:
                    file.write(human_name + '\t' + cloth_name + '\n')
            else:
                with open(test_pairs_path, 'w') as file:
                    file.write(human_name + '\t' + cloth_name + '\n')
                    
    ## make test_unpairs.txt
    random.shuffle(test_cloth_paths)
    for categorie in categories:
        test_unpairs_path = os.path.join(config.output_path, categorie, test_unpairs_name)
        
        for i in tqdm(range(0, len(test_file_paths), 2)):
            human_path = test_file_paths[i]
            cloth_path = test_cloth_paths[i]
            
            human_name = human_path.split('/')[-1]
            cloth_name = cloth_path.split('/')[-1]
            
            if os.path.exists(test_unpairs_path):
                with open(test_unpairs_path, 'a') as file:
                    file.write(human_name + '\t' + cloth_name + '\n')
            else:
                with open(test_unpairs_path, 'w') as file:
                    file.write(human_name + '\t' + cloth_name + '\n')
    
if __name__ == "__main__":
    config = get_config()
    seed_everything(config.seed)
    
    split_dataset(config)