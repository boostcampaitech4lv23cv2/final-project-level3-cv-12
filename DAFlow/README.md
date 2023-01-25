## Prepare to use

- Datasets: DressCode Dataset
- Base Checkpoints: [ckpt_viton.pt](https://ofa-beijing.oss-cn-beijing.aliyuncs.com/checkpoints/ckpt_viton.pt)
- python 3.6
- pytorch1.7
- torchvision 0.8

Download weights(vgg, alex, squeeze):
```shell
./get_weights.sh
```

Drawing img_agnostic(use data_preprocessing/get_agnostic_v3.0.py):
```python
python get_agnostic_v3.0.py
```


## Train
```python
python train_SDAFNet_viton.py {--name} {--project_name} {-b} {--dataset_dir} {--dataset_imgpath}
```

- example code
  ```python
  python train_SDAFNet_viton.py --name model_256 --project_name DAFlow_train -b 4 --dataset_dir '/opt/ml/final/data/dress_code' --dataset_imgpath 'dresses' 'upper_body' 'lower_body'
  ```


## Inference
```python
python test_SDAFNet_viton.py {--name} {-b} {--dataset_dir} {--dataset_imgpath} {--dataset_list} {-c}
```

- example code(unpair dataset)
  ```python
  python test_SDAFNet_viton.py --name test -b 4 --dataset_dir '/opt/ml/final/data/dress_code' --dataset_imgpath 'dresses' 'upper_body' 'lower_body' --dataset_list 'test_pairs_unpaired.txt' -c 'result/model_256/checkpoints/model.pt'
  ```


## Acknowledgement

Our code references the implementation of [ClotFlow](https://openaccess.thecvf.com/content_ICCV_2019/papers/Han_ClothFlow_A_Flow-Based_Model_for_Clothed_Person_Generation_ICCV_2019_paper.pdf) and [PFAPN](https://github.com/geyuying/PF-AFN), including the feature extractors, feature pyramid networks (FPN) , and the design of the cascaded structure. Thanks for their awesome works.


## License

The use of this code is RESTRICTED to non-commercial research and educational purposes.
