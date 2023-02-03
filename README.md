## Members
| <img src="https://avatars.githubusercontent.com/u/71074220?v=4" width=200> | <img src="https://avatars.githubusercontent.com/u/77265724?v=4" width=200> | <img src="https://avatars.githubusercontent.com/u/82555245?v=4" width=200> | <img src="https://avatars.githubusercontent.com/u/74371211?v=4" width=200> |
 | :-------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------: |
|                                           [김용욱](https://github.com/benelus94)                                            |                                           [최상호](https://github.com/chointer)                                            |                                            [이의석](https://github.com/Ui-Seok)                                            |                                         [이재준](https://github.com/wowns1484)

## About project
- 기획 배경: 배경~~~
- 기대 효과: 우리는 이렇게~~~

## Model architecture
그림!

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
7. `make -j 2 run_app`


## If your model saved in bentoml.models and modifying service content

1. `make run_build`
2. `make -j 2 run_app`

## Checkpoint

[DAFlow_256_192_checkpoint](https://www.dropbox.com/s/6kogpt90zgw7wxp/100_mod_all_256.pt)

[DAFlow_512_384_checkpoint](https://www.dropbox.com/s/kg9e0m6sr2j3fp0/003_allbody_512_upscale_low_lr.pt)

[Openpose](https://www.dropbox.com/sh/7xbup2qsn7vvjxo/AABWFksdlgOMXR_r5v3RwKRYa?dl=0)

[Human_parser](https://drive.google.com/u/0/uc?id=1ruJg4lqR_jgQPj-9K0PP-L2vJERYOxLP&export=download)

## Reference

- The Dress Code Dataset is proprietary to and © Yoox Net-a-Porter Group S.p.A., and its licensors. It is distributed by the University of Modena and Reggio Emilia, and available for non-commercial academic use under licence terms set out at https://github.com/aimagelab/dress-code.

- [openpose](https://github.com/Hzzone/pytorch-openpose)
- [human_parser](https://github.com/GoGoDuck912/Self-Correction-Human-Parsing)
- [carvekit](https://github.com/OPHoperHPO/image-background-remove-tool)
- [DAFlow](https://github.com/OFA-Sys/DAFlow)
- [C-VTON](https://github.com/benquick123/C-VTON)
