## How to use

1. virtual environment install (we use conda env)
2. `conda create -n {env.name}`
3. `conda activate env.name`
4. `pip install -r requirements.txt` in shell
5. `cd app`
6. `python save_model.py --model_path {checkpoint model path}`
7. `bentoml build`
8. `cd ..`
9. `make -j 2 run_app`

## if your model saved in bentoml.models and modifying service content

1. `cd app`
2. `bentoml build`
3. `cd ..`
4. `make -j 2 run_app`

## error issue
1. `importerror: libcudart.so.11.0: cannot open shared object file: no such file or directory`
sol. `conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3 -c pytorch`

## Checkpoint

[DAFlow_256_192_checkpoint](https://www.dropbox.com/s/lc90lac0ha135op/038_model_all_256_part2.pt?dl=0)

[DAFlow_512_384_checkpoint](https://www.dropbox.com/s/kg9e0m6sr2j3fp0/003_allbody_512_upscale_low_lr.pt?dl=0)

[Openpose](https://www.dropbox.com/sh/7xbup2qsn7vvjxo/AABWFksdlgOMXR_r5v3RwKRYa?dl=0)

[Human_parser](https://drive.google.com/u/0/uc?id=1k4dllHpu0bdx38J7H28rVVLpU-kOHmnH&export=download)

#### make checkpoints dir structure & path
`path` : `back-test/bentoml_v1/checkpoints`

`structure`
```
├── checkpoints
    ├── daflow
        ├── ...
    ├── human_parser
        ├── ...
    ├── openpose
        ├── ...
```