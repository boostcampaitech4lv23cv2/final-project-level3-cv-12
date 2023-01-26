## How to use

1. virtual environment install (we use conda env)
2. `conda create -n {env.name}`
3. `conda activate env.name`
4. `pip -r requirements.txt` in shell
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

## Checkpoint

[DAFlow_256_192_checkpoint](https://www.dropbox.com/s/lc90lac0ha135op/038_model_all_256_part2.pt?dl=0)

[DAFlow_512_384_checkpoint](https://www.dropbox.com/s/kg9e0m6sr2j3fp0/003_allbody_512_upscale_low_lr.pt?dl=0)