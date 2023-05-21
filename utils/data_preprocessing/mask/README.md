### 1. carvekit 설치
```
pip install carvekit --extra-index-url https://download.pytorch.org/whl/cu113
```
명령어: `$ carvekit -i {input_path} -o {output_path}`
<br/>
<br/>
### 2.1. mask data 만들기 (python module)
1) 흰 배경 이미지 생성
```
get_white_bg(path_image, threshold_pixval=230, save_name='')
```
2) 옷 위치 마스크 생성 (옷 부분은 흰색, 배경은 검은색)
```
get_binary_mask(path_image, threshold_pixval=230, save_name='')
```
`threshold_pixval`: carvekit 결과(RGBA)에서 투명도의 값이 threshold_pixval보다 작으면 배경으로 판단한다.  
`save_name`: image를 저장하고 싶을 때 파일명 (확장자 제외). 별도로 설정하지 않으면 저장되지 않는다. `.png`로 저장된다.
<br/>
### 2.2. mask data 만들기 (CLI interface)
1) `get_mask.sh`에서 `PATH_MAIN` 수정한다. `images` 폴더가 있는 폴더로 설정한다.
2) `get_mask.sh` 실행 (파일 안에 있는 명령어를 직접 수행해도 된다.)
```
sh get_mask.sh
```
<br/>
<br/>

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
