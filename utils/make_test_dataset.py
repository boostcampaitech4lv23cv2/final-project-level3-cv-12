import os
import shutil
import glob
from tqdm import tqdm
import argparse
import torch
import random
import numpy as np

def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--select-num', default=30, help='dataset select num')
    parser.add_argument('-d', '--data-root-path', default='/opt/ml/input/datasets/SplitData', help='input data root path')
    parser.add_argument('-o', '--output-root-path', default='/opt/ml/input/datasets/SplitData', help='output dir path')
    parser.add_argument('-s', '--seed', default=21, type=int, help='random seed')
    parser.add_argument('-m', '--mode', default='copy', help='select mode "copy" or "move"')
    parser.add_argument('-r', '--raw_dataset', default='False', help='check original Dress-code dataset')
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

def select_test_dataset(config):
    categories = ['upper_body', 'lower_body', 'dresses']
    
    if config.raw_dataset == 'True':
        sub_dirs = ['keypoints', 'label_maps', 'skeletons', 'dense', 'images']
    else:
        sub_dirs = ['agnostic', 'parse_agnostic', 'keypoints', 'label_maps', 'skeletons', 'dense', 'images']
        
    phases = ['test_pair', 'test_unpair']
    
    pair_out_dir_path = f'{config.output_root_path}/{phases[0]}'
    unpair_out_dir_path = f'{config.output_root_path}/{phases[1]}'
    
    ## make output dirs
    for phase in phases:
        for categorie in categories:
            for sub_dir in sub_dirs:
                os.makedirs(os.path.join(config.output_root_path, phase, categorie, sub_dir), exist_ok=True)
        
    for categorie in tqdm(categories):    
        pair_path = f'{config.data_root_path}/{categorie}/test_pairs_paired.txt'
        unpair_path = f'{config.data_root_path}/{categorie}/test_pairs_unpaired.txt'

        with open(pair_path, 'r') as f:
            test_pair_paths = f.readlines()
            random.shuffle(test_pair_paths)
            test_pair_paths = test_pair_paths[:config.select_num]
            
        with open(unpair_path, 'r') as f:
            test_unpair_paths = f.readlines()
            random.shuffle(test_unpair_paths)
            test_unpair_paths = test_unpair_paths[:config.select_num]
        
        ## pairs phase
        for test_pair_path in tqdm(test_pair_paths):
            file_id = test_pair_path.split('_')[0]

            for sub_dir in sub_dirs:
                file_paths = glob.glob(f'{config.data_root_path}/{categorie}/{sub_dir}/{file_id}*')
                
                for file_path in file_paths:
                    file_name = file_path.split('/')[-1]
                    if config.mode == 'copy':
                        shutil.copy2(file_path, os.path.join(pair_out_dir_path, categorie, sub_dir, file_name))
                    elif config.mode == 'move':
                        shutil.move(file_path, os.path.join(pair_out_dir_path, categorie, sub_dir, file_name))
                            
        ## unpairs phase
        for test_unpair_path in tqdm(test_unpair_paths):
            test_unpair_path = test_unpair_path.rstrip('\n').split('\t')
            human_id, cloth_id = test_unpair_path[0].split('_')[0], test_unpair_path[1].split('_')[0]

            for sub_dir in sub_dirs:
                if sub_dir == 'images':
                    file_paths = glob.glob(f'{config.data_root_path}/{categorie}/{sub_dir}/{human_id}_0*')
                    file_paths += glob.glob(f'{config.data_root_path}/{categorie}/{sub_dir}/{cloth_id}_1*')
                else:
                    file_paths = glob.glob(f'{config.data_root_path}/{categorie}/{sub_dir}/{human_id}*')
                
                for file_path in file_paths:
                    file_name = file_path.split('/')[-1]
                    if config.mode == 'copy':
                        shutil.copy2(file_path, os.path.join(unpair_out_dir_path, categorie, sub_dir, file_name))
                    elif config.mode == 'move':
                        shutil.move(file_path, os.path.join(unpair_out_dir_path, categorie, sub_dir, file_name))
                
if __name__ == "__main__":
    config = get_config()
    seed_everything(config.seed)
    
    select_test_dataset(config)