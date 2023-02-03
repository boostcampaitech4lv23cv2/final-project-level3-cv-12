## How to use

1. `poetry install`
2. `poetry shell`
3. `conda activate env.name`
4. `pip install -r requirements.txt` in shell
5. `conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3 -c pytorch`
6. `cd app`
7. `python save_model.py --daflow-path {path} --openpose-path {path} --parser-path {path} (checkpoint model path)`
8. `bentoml build`
9. `cd ..`
10. `make -j 2 run_app`

## if your model saved in bentoml.models and modifying service content

1. `cd app`
2. `bentoml build`
3. `cd ..`
4. `make -j 2 run_app`

## Checkpoint

[DAFlow_256_192_checkpoint](https://www.dropbox.com/s/6kogpt90zgw7wxp/100_mod_all_256.pt)

[DAFlow_512_384_checkpoint](https://www.dropbox.com/s/kg9e0m6sr2j3fp0/003_allbody_512_upscale_low_lr.pt)

[Openpose](https://www.dropbox.com/sh/7xbup2qsn7vvjxo/AABWFksdlgOMXR_r5v3RwKRYa?dl=0)

[Human_parser](https://www.dropbox.com/s/w6rgpnjyp11j6fr/exp-schp-201908301523-atr.pth)

## make checkpoints dir structure & path
`path` : `server/bentoml_v1/checkpoints`

## Folder structure
```
├── app/
│   ├── modules/
│   │   ├── agnostic/
│   │   ├── carvekit_custom/
│   │   ├── human_parser/
│   │   ├── openpose/
│   │   ├── model.py
│   │   └── preprocess.py
│   ├── bentofile.yaml
│   ├── README.md
│   ├── save_model.py
│   └── service.py
├── checkpoints/
│   ├── daflow/
│   │   ├── ...
│   ├── human_parser/
│   │   ├── ...
│   └── openpose/
│       ├── ...
└── sample_images/
    ├── dress/
    │   └── etc/
    │       ├── agnostic/
    │       ├── images/
    │       ├── skeletons/
    │       ├── Woman_a.jpg
    │       ├── ...
    │       └── Woman_e.jpg
    ├── long/
    │   └── ...
    └── short/
        └── ...
```
