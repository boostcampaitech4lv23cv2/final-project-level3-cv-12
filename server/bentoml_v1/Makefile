run_black:
	python3 -m black . -l 119

run_server:
	bentoml serve vton_daflow:latest --port 8501

run_client:
	python3 -m streamlit run app/homepage.py --server.port 30003 --server.fileWatcherType none

run_app: run_server run_client

run_assignment_tests:
	poetry run pytest assignments/app_test.py