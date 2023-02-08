run_checkpoints_download:
	mkdir service/back-end/checkpoints/daflow
	mkdir service/back-end/checkpoints/human_parser
	mkdir service/back-end/checkpoints/openpose
	wget https://www.dropbox.com/s/6kogpt90zgw7wxp/100_mod_all_256.pt -P ./service/back-end/checkpoints/daflow/
	wget https://www.dropbox.com/s/kg9e0m6sr2j3fp0/003_allbody_512_upscale_low_lr.pt -P ./service/back-end/checkpoints/daflow
	wget https://www.dropbox.com/sh/7xbup2qsn7vvjxo/AABWFksdlgOMXR_r5v3RwKRYa?dl=0 -P ./service/back-end/checkpoints/openpose -O Openpose.zip
	unzip ./service/back-end/checkpoints/openpose/Openpose.zip -x ./service/back-end/checkpoints/openpose/
	wget https://www.dropbox.com/s/w6rgpnjyp11j6fr/exp-schp-201908301523-atr.pth -P ./service/back-end/checkpoints/human_parser

run_server:
	bentoml serve vton_daflow:latest --port 8501

run_client:
	python3 -m streamlit run service/front-end/homepage.py --server.port 30003 --server.fileWatcherType none

run_server_warmup:
	python service/back-end/app/warmup_server.py

run_save_model:
	python service/back-end/app/save_model.py

run_apt_install:
	apt-get install -y gcc-8
	apt-get install -y g++
	apt-get -y install libgl1-mesa-glx

run_build:
	bentoml build -f service/back-end/app/bentofile.yaml service/back-end/app

run_app: run_server run_client run_server_warmup
