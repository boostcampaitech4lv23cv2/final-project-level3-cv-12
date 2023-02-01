## How to run server

1. `poetry shell`
2. `poetry install`
3. `make run_apt_install`
4. `download models checkpoints`
5. `python service/back-end/app/save_model.py --daflow-path {path} --openpose-path {path} --parser-path {path} (checkpoint model path)`
6. `make run_build`
7. `make -j 2 run_app`


## if your model saved in bentoml.models and modifying service content

1. `make run_build`
2. `make -j 2 run_app`

## Checkpoint

[DAFlow_256_192_checkpoint](https://www.dropbox.com/s/lc90lac0ha135op/038_model_all_256_part2.pt?dl=0)

[DAFlow_512_384_checkpoint](https://www.dropbox.com/s/kg9e0m6sr2j3fp0/003_allbody_512_upscale_low_lr.pt?dl=0)

[Openpose](https://www.dropbox.com/sh/7xbup2qsn7vvjxo/AABWFksdlgOMXR_r5v3RwKRYa?dl=0)

[Human_parser](https://drive.google.com/u/0/uc?id=1ruJg4lqR_jgQPj-9K0PP-L2vJERYOxLP&export=download)

#### make checkpoints dir structure & path
`path` : `server/bentoml_v1/checkpoints` (we used path)