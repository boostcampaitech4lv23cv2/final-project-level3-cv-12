
```
├── README.md
├── human_parser : about human parser modules
├── openpose : about openpose modules
├── bentofile.yaml : bentoml build config
├── confirm_button_hack.py
├── frontend.py : Streamlit으로 작성한 프론트엔드
├── model.py : 딥러닝 모델
├── preprocess.py : cloth, human image preprocess modules
├── save_model.py : Saving Models with BentoML
└── service.py : backend service
```

#### 1. Cloth 업로드 
예상 아바타 디렉터리 구조를 구상 중으로 get_avatar 함수 인풋으로 avatar_id, avatar_path 필요 ex) avatar_path=`dresses/avatar`
├── avatar
    ├── agnostic
        ├── 000000_0.jpg
        ├── 000001_0.jpg
        ├── 000002_0.jpg
        ├── ...
    ├── images
        ├── ...
    ├── skeleton
        ├── ...
    ├── label_map
        ├── ...
    ├── keypoints
        ├── ...
    ├── etc ...

#### 2. Cloth && Human 업로드
업로드 된 두 가지 이미지를 requests로 전달