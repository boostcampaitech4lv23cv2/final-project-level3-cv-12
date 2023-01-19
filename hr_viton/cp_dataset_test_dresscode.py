import torch
import torch.utils.data as data
import torchvision.transforms as transforms

from PIL import Image, ImageDraw

import os.path as osp
import numpy as np
import json


class CPDatasetTest(data.Dataset):
    """
        Test Dataset for CP-VTON.
    """
    def __init__(self, opt):
        super(CPDatasetTest, self).__init__()
        # base setting
        self.opt = opt
        self.root = opt.dataroot
        self.datamode = opt.datamode # train or test or self-defined
        self.data_list = opt.data_list
        self.fine_height = opt.fine_height
        self.fine_width = opt.fine_width
        self.semantic_nc = opt.semantic_nc
        self.data_path = opt.dataroot  # DressCode
        self.transform = transforms.Compose([  \
                transforms.ToTensor(),   \
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

        # load data list
        im_names = []
        c_names = []
        with open(osp.join(opt.dataroot, opt.data_list), 'r') as f:
            for line in f.readlines():
                im_name, c_name = line.strip().split()
                ## DressCode
                im_names.append(im_name.split('_')[0])
                c_names.append(c_name.split('_')[0])

        self.im_names = im_names
        self.c_names = dict()
        self.c_names['paired'] = im_names
        self.c_names['unpaired'] = c_names
        
    def name(self):
        return "CPDataset"
    
    def __getitem__(self, index):
        im_name = self.im_names[index]
        c_name = {}
        c = {}
        cm = {}
        for key in self.c_names:
            c_name[key] = self.c_names[key][index]
            c[key] = Image.open(osp.join(self.data_path, 'images', c_name[key] + '_1.jpg')).convert('RGB')  ## DressCode
            c[key] = transforms.Resize(self.fine_width, interpolation=2)(c[key])
            cm[key] = Image.open(osp.join(self.data_path, 'cloth_mask', c_name[key] + '_7.jpg'))  ## DressCode
            cm[key] = transforms.Resize(self.fine_width, interpolation=0)(cm[key])

            c[key] = self.transform(c[key])  # [-1,1]
            cm_array = np.array(cm[key])
            cm_array = (cm_array >= 128).astype(np.float32)
            cm[key] = torch.from_numpy(cm_array)  # [0,1]
            cm[key].unsqueeze_(0)

        # person image
        im_pil_big = Image.open(osp.join(self.data_path, 'images', im_name + '_0.jpg'))   ## DressCode
        im_pil = transforms.Resize(self.fine_width, interpolation=2)(im_pil_big)
        
        im = self.transform(im_pil)

        # load parsing image
        im_parse_pil_big = Image.open(osp.join(self.data_path, 'label_maps', im_name + '_4.png'))   ## DressCode
        im_parse_pil = transforms.Resize(self.fine_width, interpolation=0)(im_parse_pil_big)
        parse = torch.from_numpy(np.array(im_parse_pil)[None]).long()
        im_parse = self.transform(im_parse_pil.convert('RGB'))

        ## DressCode
        labels = {
            0:  ['background',  [0]],   # neck(Jumpsuits)가 없어서 제외했는데, 나중에 문제가 생길 수 있다.
            1:  ['hair',        [1, 2]],
            2:  ['face',        [3, 11]],
            3:  ['upper',       [4, 7]],
            4:  ['bottom',      [5, 6, 8]],
            5:  ['left_arm',    [14]],
            6:  ['right_arm',   [15]],
            7:  ['left_leg',    [12]],
            8:  ['right_leg',   [13]],
            9:  ['left_shoe',   [9]],
            10: ['right_shoe',  [10]],
            11: ['socks',       []],
            12: ['noise',       [16, 17]]
        }

        parse_map = torch.FloatTensor(18, self.fine_height, self.fine_width).zero_()  ## DressCode; 20 -> 18
        parse_map = parse_map.scatter_(0, parse, 1.0)
        new_parse_map = torch.FloatTensor(self.semantic_nc, self.fine_height, self.fine_width).zero_()
        
        for i in range(len(labels)):
            for label in labels[i][1]:
                new_parse_map[i] += parse_map[label]
        
        parse_onehot = torch.FloatTensor(1, self.fine_height, self.fine_width).zero_()
        for i in range(len(labels)):
            for label in labels[i][1]:
                parse_onehot[0] += parse_map[label] * i

        # load image-parse-agnostic
        #image_parse_agnostic = Image.open(osp.join(self.data_path, 'parse_agnostic', im_name + '_0.jpg'))  ## DressCode
        image_parse_agnostic = Image.open(osp.join(self.data_path, 'parse_agnostic_png', im_name + '_0.png'))  ## DressCode
        image_parse_agnostic = transforms.Resize(self.fine_width, interpolation=0)(image_parse_agnostic)
        parse_agnostic = torch.from_numpy(np.array(image_parse_agnostic)[None]).long()
        image_parse_agnostic = self.transform(image_parse_agnostic.convert('RGB'))

        parse_agnostic_map = torch.FloatTensor(18, self.fine_height, self.fine_width).zero_()  ## DressCode; 20 -> 18
        parse_agnostic_map = parse_agnostic_map.scatter_(0, parse_agnostic, 1.0)
        new_parse_agnostic_map = torch.FloatTensor(self.semantic_nc, self.fine_height, self.fine_width).zero_()
        for i in range(len(labels)):
            for label in labels[i][1]:
                new_parse_agnostic_map[i] += parse_agnostic_map[label]
                

        # parse cloth & parse cloth mask
        pcm = new_parse_map[3:4]
        im_c = im * pcm + (1 - pcm)
        
        # load pose points
        pose_map = Image.open(osp.join(self.data_path, 'skeletons', im_name + '_5.jpg'))   ## DressCode
        pose_map = transforms.Resize(self.fine_width, interpolation=2)(pose_map)
        pose_map = self.transform(pose_map)  # [-1,1]
        
        with open(osp.join(self.data_path, 'keypoints', im_name + '_2.json'), 'r') as f:   ## DressCode
            pose_label = json.load(f)
            pose_data = np.array(pose_label['keypoints'])[:, :2] * 2   # scale 차이가 있어서 * 2 해준다. (아마 visualize 외에는 쓰이지도 않을 것)
        
        # load densepose
        densepose_map = Image.open(osp.join(self.data_path, 'dense', im_name + '_5.png'))    ## DressCode
        densepose_map = transforms.Resize(self.fine_width, interpolation=2)(Image.fromarray(np.repeat(np.array(densepose_map)[:, :, np.newaxis], 3, -1))) # TODO dirty
        densepose_map = self.transform(densepose_map)  # [-1,1]
        ## DressCode
        agnostic = Image.open(osp.join(self.data_path, 'agnostic', im_name + '_0.jpg'))    ## DressCode
        agnostic = transforms.Resize(self.fine_width, interpolation=2)(agnostic)
        agnostic = self.transform(agnostic)
        


        result = {
            'c_name':   c_name,     # for visualization
            'im_name':  im_name,    # for visualization or ground truth
            # intput 1 (clothfloww)
            'cloth':    c,          # for input
            'cloth_mask':     cm,   # for input
            # intput 2 (segnet)
            'parse_agnostic': new_parse_agnostic_map,
            'densepose': densepose_map,
            'pose': pose_map,       # for conditioning
            # GT
            'parse_onehot' : parse_onehot,  # Cross Entropy
            'parse': new_parse_map, # GAN Loss real
            'pcm': pcm,             # L1 Loss & vis
            'parse_cloth': im_c,    # VGG Loss & vis
            # visualization
            'image':    im,         # for visualization
            'agnostic' : agnostic
            }
        
        return result

    def __len__(self):
        return len(self.im_names)


class CPDataLoader(object):
    def __init__(self, opt, dataset):
        super(CPDataLoader, self).__init__()
        if opt.shuffle :
            train_sampler = torch.utils.data.sampler.RandomSampler(dataset)
        else:
            train_sampler = None

        self.data_loader = torch.utils.data.DataLoader(
                dataset, batch_size=opt.batch_size, shuffle=(train_sampler is None),
                num_workers=opt.workers, pin_memory=True, drop_last=True, sampler=train_sampler)
        self.dataset = dataset
        self.data_iter = self.data_loader.__iter__()

    def next_batch(self):
        try:
            batch = self.data_iter.__next__()
        except StopIteration:
            self.data_iter = self.data_loader.__iter__()
            batch = self.data_iter.__next__()

        return batch