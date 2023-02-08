## Members


| <img src="https://avatars.githubusercontent.com/u/71074220?v=4" width=200> | <img src="https://avatars.githubusercontent.com/u/77265724?v=4" width=200> | <img src="https://avatars.githubusercontent.com/u/82555245?v=4" width=200> | <img src="https://avatars.githubusercontent.com/u/74371211?v=4" width=200> |
| :--------------------------------------------------------------------------: | :--------------------------------------------------------------------------: | :--------------------------------------------------------------------------: | :--------------------------------------------------------------------------: |
|                   [김용욱](https://github.com/benelus94)                   |                   [최상호](https://github.com/chointer)                   |                    [이의석](https://github.com/Ui-Seok)                    |                   [이재준](https://github.com/wowns1484)                   |

## About project

- 기획 배경

  많은 사람들이 온라인 쇼핑몰을 통해 옷을 구매하는데 상품 상세 보기를 누르면 모델 없이
  옷에 대한 소개만 있는 쇼핑몰 페이지가 존재하였습니다.
  저희는 여기에 불편함을 느껴 이를 해소하고자 사용자가 원하는 옷을 가상의 모델 혹은 사용자의 모델에 착용한 모습을 볼 수 있도록 하는 프로젝트를 기획하게 되었습니다.
- 기대 효과

  소비자의 구매 만족도 상승 및 반품량 감소

  판매자의 피팅 사진 제작 비용 감소

## Model architecture

![model architecture](https://user-images.githubusercontent.com/82555245/217208254-bbee6e34-896b-4e91-811d-38f3365f0f7e.png)
> [DAFlow paper](https://arxiv.org/abs/2207.09161)

## Dataset

- [Dress Code dataset](https://github.com/aimagelab/dress-code)

## Equipments

- CPU: Intel(R) Xeon(R) Gold 5120 CPU @ 2.20GHz
- GPU: V100 32GB
- OS: Ubuntu 18.04 LTS

## Folder structure

```
├── DAFlow/
│   ├── models/
│   │   ├── external_function.py
│   │   └── sdafnet.py
│   ├── utils/
│   │   ├── lpips/
│   │   ├── metrics.py
│   │   ├── test_ssim.py
│   │   └── utils.py
│   ├── dataset.py
│   ├── get_weigths.sh
│   ├── README.md
│   ├── test_SDAFNet_viton.py
│   └── train_SDAFNet_viton.py
├── service/
│   ├── back-end/
│   └── front-end/
├── utils/
│   └── data_preprocessing/
│       ├── agnostic/
│       │   ├── v1.0
│       │   ├── v2.0
│       │   ├── get_agnostic_v3.1.py
│       │   └── README.md
│       ├── mask/
│       │   ├── get_mask_module.py
│       │   ├── get_mask.py
│       │   ├── get_mask.sh
│       │   └── READMD.md
│       ├── export_tensor.sh
│       ├── export_torch.sh
│       ├── make_test_dataset.py
│       ├── pkl_to_png.py
│       └── split_dataset.py
├── .gitignore
├── Makefile
├── poetry.lock
├── pyproject.toml
└── README.md
```

## How to run server

1. `poetry shell`
2. `poetry install`
3. `make run_apt_install`
4. `make run_checkpoints_download`
5. `python service/back-end/app/save_model.py --daflow-path {path} --openpose-path {path} --parser-path {path} (checkpoint model path)`
6. `make run_build`
7. `make -j 3 run_app`

## If your model saved in bentoml.models and modifying service content

1. `make run_build`
2. `make -j 3 run_app`

## Reference

- The Dress Code Dataset is proprietary to and © Yoox Net-a-Porter Group S.p.A., and its licensors. It is distributed by the University of Modena and Reggio Emilia, and available for non-commercial academic use under licence terms set out at https://github.com/aimagelab/dress-code.
- [openpose](https://github.com/Hzzone/pytorch-openpose)
- [human_parser](https://github.com/GoGoDuck912/Self-Correction-Human-Parsing)
- [carvekit](https://github.com/OPHoperHPO/image-background-remove-tool)
- [DAFlow](https://github.com/OFA-Sys/DAFlow)
- [C-VTON](https://github.com/benquick123/C-VTON)
