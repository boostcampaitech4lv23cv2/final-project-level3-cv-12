run_server:
	bentoml serve vton_daflow:latest --port 8502

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