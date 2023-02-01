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

[DAFlow_256_192_checkpoint](https://www.dropbox.com/s/lc90lac0ha135op/038_model_all_256_part2.pt?dl=0)

[DAFlow_512_384_checkpoint](https://www.dropbox.com/s/kg9e0m6sr2j3fp0/003_allbody_512_upscale_low_lr.pt?dl=0)

[Openpose](https://www.dropbox.com/sh/7xbup2qsn7vvjxo/AABWFksdlgOMXR_r5v3RwKRYa?dl=0)

[Human_parser](https://drive.google.com/u/0/uc?id=1ruJg4lqR_jgQPj-9K0PP-L2vJERYOxLP&export=download)

#### make checkpoints dir structure & path
`path` : `server/bentoml_v1/checkpoints`

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