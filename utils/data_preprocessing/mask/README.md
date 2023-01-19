### 1. carvekit 설치
```
pip install carvekit --extra-index-url https://download.pytorch.org/whl/cu113
```
명령어: `$ carvekit -i {input_path} -o {output_path}`



### 2. mask data 만들기
1) `get_mask.sh`에서 `PATH_MAIN` 수정한다. `images` 폴더가 있는 폴더로 설정한다.
2) `get_mask.sh` 실행 (파일 안에 있는 명령어를 직접 수행해도 된다.)
```
sh get_mask.sh
```



### 3. `get_mask.sh` process
1) 사용할 폴더 만들기
    `temp_image_cloth`: 옷 image를 옮겨두는 폴더
    `temp_image_cloth_rmbkg`: carvekit 결과물을 저장하는 폴더
    `cloth_mask`: 최종 결과 mask를 저장하는 폴더

2) background-removed(rmbkg) images 만들기 (~40분/5000장)
    (1) 옷 이미지를 임시 폴더에 이동
    (2) carvekit으로 rmbkg images 만들기
    (3) 옷 이미지를 다시 원래 폴더로 이동
     * `temp_image_cloth` 폴더는 삭제해도 된다.
    
3) bkg_removed image에서 mask image(jpg) 만들기 (~4.5분/5000장)
    `get_mask.py` 실행


notion: https://www.notion.so/Clothing-Mask-e4d66f3cf91d4d868e04f442c7cfc16f
