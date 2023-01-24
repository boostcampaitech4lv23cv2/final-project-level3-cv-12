## About this folder
Virtual Try-On을 하는 대부분의 모델들은 human-parsing과 pose 정보를 통해 human image에 masking을 한 이미지가 필요로함
따라서 모델에 필요한 데이터를 만들어내기 위한 코드임
> DressCode Github의 코드를 활용함


## Need library
1. numpy >= 1.19.2
2. Pillow >= 9.1.0
3. torch >= 1.7.1
4. torchvision >= 0.8.2
5. opencv-python >= 4.7.0.68
6. tqdm, json


## How to use
```python
python get_agnostic_v3.1.py --{data_path} --{part}
```