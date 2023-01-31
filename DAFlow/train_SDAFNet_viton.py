import sys, os
import tqdm
import argparse

import torch
from torch import nn
import torch.backends.cudnn as cudnn
from torch.nn import functional as F
from torchvision import utils
from torch.utils import data

from datasets import DressCodeDataset
from models.sdafnet import SDAFNet_Tryon
from models import external_function
from utils import lpips
from utils.utils import AverageMeter

import wandb

sys.path.append('../C-VTON/utils')
from metrics import inception_score, ssim #fid

def get_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, required=True)
    parser.add_argument('--project_name', type=str, default='DAFlow', help='wandb project name')
    parser.add_argument('--entity', type=str, default='cv12-final-project', help='wandb team repository name')

    parser.add_argument('-b', '--batch_size', type=int, default=4)
    parser.add_argument('--lr', type=float, default=0.00005)
    parser.add_argument('--epoch', type=str, default=200)
    parser.add_argument('-j', '--workers', type=int, default=4)

    parser.add_argument('--load_height', type=int, default=256)
    parser.add_argument('--load_width', type=int, default=192)
    parser.add_argument('--shuffle', action='store_false')

    parser.add_argument('--dataset_dir', type=str, default='../data/dress_code')
    parser.add_argument('--dataset_imgpath', nargs='+', default=['upper_body'])
    parser.add_argument('--dataset_train_list', type=str, default='train_pairs.txt')
    parser.add_argument('--dataset_val_list', type=str, default='test_pairs_paired.txt')

    parser.add_argument('--use_checkpoint', action='store_true')
    parser.add_argument('-c', '--checkpoint_dir', type=str, default='./ckpt_viton.pt')

    parser.add_argument('--save_dir', type=str, default='./results/')
    parser.add_argument('--display_freq', type=int, default=200)
    parser.add_argument('--save_freq', type=int, default=10)

    parser.add_argument('--multi_flows', type=int, default=6)

    opt = parser.parse_args()
    return opt


def train(opt, net):
    train_dataset = DressCodeDataset(opt, mode='train')
    train_loader = data.DataLoader(train_dataset, batch_size=opt.batch_size, drop_last=True, shuffle=opt.shuffle, num_workers=opt.workers)
    val_dataset = DressCodeDataset(opt, mode='val')
    val_loader = data.DataLoader(val_dataset, batch_size=opt.batch_size, drop_last=True, shuffle=opt.shuffle, num_workers=opt.workers)

    #wandb setting
    wandb.init(project=opt.project_name,
               name=opt.name,
               entity=opt.entity)
    wandb.config.update(opt)

    #criterion
    criterion_L1 = nn.L1Loss()
    criterion_percept = lpips.exportPerceptualLoss(model="net-lin", net="vgg", use_gpu=True)
    criterion_style = external_function.VGGLoss().cuda()

    #optimizer
    optimizer = torch.optim.AdamW(net.parameters(), lr=opt.lr)

    #scheduler
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.2)

    iterations = 0
    for epoch in range(1, opt.epoch):
        print(f"### Start {epoch}/{opt.epoch} Train ###")

        train_loss_all = AverageMeter()
        train_loss_l1 = AverageMeter()
        train_loss_vgg = AverageMeter()
        train_is = AverageMeter()
        train_ssim = AverageMeter()
        val_loss_all = AverageMeter()
        val_loss_l1 = AverageMeter()
        val_loss_vgg = AverageMeter()
        val_is = AverageMeter()
        val_ssim = AverageMeter()
        
        ### Train Loop ###
        net.train()
        for i, inputs in enumerate(tqdm.tqdm(train_loader)):
            iterations+=1

            img = inputs['img'].cuda()
            img_agnostic = inputs['img_agnostic'].cuda()
            pose = inputs['pose'].cuda()
            cloth_img = inputs['cloth'].cuda()

            img =  F.interpolate(img, size=(opt.load_height, opt.load_width), mode='bilinear')
            ref_input = torch.cat((pose, img_agnostic), dim=1)
            result_tryon, results_all = net(ref_input, cloth_img, img_agnostic, return_all=True)

            # loss
            loss_all = 0
            loss_l1_stack = 0
            loss_vgg_stack = 0
            num_layer = 5
            for num in range(num_layer):
                cur_img = F.interpolate(img, scale_factor=0.5**(4-num), mode='bilinear')
                loss_l1 = criterion_L1(results_all[num], cur_img.cuda())

                if num == 0:
                    cur_img = F.interpolate(cur_img, scale_factor=2, mode='bilinear')
                    results_all[num] = F.interpolate(results_all[num], scale_factor=2, mode='bilinear')

                loss_perceptual = criterion_percept(cur_img.cuda(),results_all[num]).mean()
                loss_content, loss_style = criterion_style(results_all[num], cur_img.cuda())
                loss_vgg = loss_perceptual+100*loss_style+0.1*loss_content

                loss_all = loss_all + (num+1)*loss_l1 + (num+1)*loss_vgg
                loss_l1_stack = loss_l1_stack + (num+1)*loss_l1
                loss_vgg_stack = loss_vgg_stack + (num+1)*loss_vgg

            optimizer.zero_grad()
            loss_all.backward()
            optimizer.step()

            # update
            train_ssim.update(ssim(img, result_tryon).item(), n=opt.batch_size)
            train_is.update(inception_score(result_tryon, batch_size=opt.batch_size)[0], n=opt.batch_size)
            train_loss_all.update(loss_all.item(), n=opt.batch_size)
            train_loss_l1.update(loss_l1_stack.item(), n=opt.batch_size)
            train_loss_vgg.update(loss_vgg_stack.item(), n=opt.batch_size)

            if iterations % opt.display_freq == 1:
                parse_pred = torch.cat([cloth_img, img_agnostic, result_tryon, img], 2)
                parse_pred = F.interpolate(parse_pred, size=(1024, 192), mode='bilinear')
                utils.save_image(
                        parse_pred,
                        f"{os.path.join(opt.save_dir, opt.name)}/log_images/{str(iterations).zfill(6)}_{str(opt.name)}.jpg",
                        nrow=6,
                        normalize=True,
                        range=(-1, 1),
                    )
            
            wandb.log({
                "epoch": epoch,
                "iteration": iterations,
                "learning_rate": optimizer.param_groups[0]['lr'],
                
                "train_loss": train_loss_all.avg,
                "train_loss_l1": train_loss_l1.avg,
                "train_loss_vgg": train_loss_vgg.avg,
                "train_is": train_is.avg,
                "train_ssim": train_ssim.avg,
            })

        # save
        if epoch % opt.save_freq == 0:
            torch.save(
                {
                    "state_dict": net.state_dict(),
                    "optim": optimizer.state_dict(),
                    "opt": opt,
                },
                f"{os.path.join(opt.save_dir, opt.name)}/checkpoints/{str(epoch).zfill(3)}_{str(opt.name)}.pt",
            )

        print(f"[{epoch:3}/{opt.epoch:3}][{iterations}] TRAIN.  loss={train_loss_all.avg:<10.4f}loss_l1={train_loss_l1.avg:<10.4f}loss_vgg={train_loss_vgg.avg:<10.4f}IS={train_is.avg:<10.4f}SSIM={train_ssim.avg:<10.4f}")
        
        scheduler.step()

        
        ### Validation Loop ###
        net.eval()
        with torch.no_grad():
            for i, inputs in enumerate(tqdm.tqdm(val_loader)):
                img = inputs['img'].cuda()  # normalize image
                img_agnostic = inputs['img_agnostic'].cuda() # Masked model image
                pose = inputs['pose'].cuda()
                cloth_img = inputs['cloth'].cuda()

                img =  F.interpolate(img, size=(opt.load_height, opt.load_width), mode='bilinear')
                cloth_img = F.interpolate(cloth_img, size=(opt.load_height, opt.load_width), mode='bilinear')
                img_agnostic = F.interpolate(img_agnostic, size=(opt.load_height, opt.load_width), mode='bilinear')
                pose = F.interpolate(pose, size=(opt.load_height, opt.load_width), mode='bilinear')
                ref_input = torch.cat((pose, img_agnostic), dim=1)

                result_tryon, results_all = net(ref_input, cloth_img, img_agnostic, return_all=True)

                # loss
                loss_all = 0
                loss_l1_stack = 0
                loss_vgg_stack = 0
                num_layer = 5
                for num in range(num_layer):
                    cur_img = F.interpolate(img, scale_factor=0.5**(4-num), mode='bilinear')
                    loss_l1 = criterion_L1(results_all[num], cur_img.cuda())

                    if num == 0:
                        cur_img = F.interpolate(cur_img, scale_factor=2, mode='bilinear')
                        results_all[num] = F.interpolate(results_all[num], scale_factor=2, mode='bilinear')

                    loss_perceptual = criterion_percept(cur_img.cuda(),results_all[num]).mean()
                    loss_content, loss_style = criterion_style(results_all[num], cur_img.cuda())
                    loss_vgg = loss_perceptual+100*loss_style+0.1*loss_content

                    loss_all = loss_all + (num+1) * loss_l1 + (num + 1)  * loss_vgg
                    loss_l1_stack = loss_l1_stack + (num+1)*loss_l1
                    loss_vgg_stack = loss_vgg_stack + (num+1)*loss_vgg

                # update
                val_ssim.update(ssim(img, result_tryon).item(), n=opt.batch_size)
                val_is.update(inception_score(result_tryon, batch_size=opt.batch_size)[0], n=opt.batch_size)
                val_loss_all.update(loss_all.item(), n=opt.batch_size)
                val_loss_l1.update(loss_l1_stack.item(), n=opt.batch_size)
                val_loss_vgg.update(loss_vgg_stack.item(), n=opt.batch_size)

            # logging
            wandb.log({
                "epoch": epoch,
                "iteration": iterations,

                "val_loss": val_loss_all.avg,
                "val_loss_l1": val_loss_l1.avg,
                "val_loss_vgg": val_loss_vgg.avg,
                "val_is": val_is.avg,
                "val_ssim": val_ssim.avg
            })

            print(f"[{epoch:3}/{opt.epoch:3}][{iterations}] VAL.    loss={val_loss_all.avg:<10.4f}loss_l1={val_loss_l1.avg:<10.4f}loss_vgg={val_loss_vgg.avg:<10.4f} IS={val_is.avg:<10.4f}SSIM={val_ssim.avg:<10.4f}")


def main():
    opt = get_opt()
    print(opt)

    os.makedirs(os.path.join(opt.save_dir, opt.name, 'log_images'), exist_ok=True)
    os.makedirs(os.path.join(opt.save_dir, opt.name, 'checkpoints'), exist_ok=True)

    if not os.path.exists(opt.save_dir):
        os.makedirs(opt.save_dir)

    sdafnet = SDAFNet_Tryon(ref_in_channel=opt.multi_flows)
    sdafnet = sdafnet.cuda()

    if opt.use_checkpoint:
        model_path = opt.checkpoint_dir
        if model_path == 'ckpt_viton.pt':
            sdafnet.load_state_dict(torch.load(model_path))
        else:
            checkpoint = torch.load(model_path)
            sdafnet.load_state_dict(checkpoint['state_dict'])
    sdafnet.train()
    cudnn.benchmark = True
    train(opt, sdafnet)


if __name__ == '__main__':
    main()
