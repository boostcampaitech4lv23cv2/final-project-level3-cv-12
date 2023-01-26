from model import get_model
import bentoml
import argparse

def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model-path', default='/opt/ml/input/038_model_all_256_part2.pt', help='saved model path')
    config = parser.parse_args()
    
    return config

if __name__ == "__main__":
    config = get_config()
    model = get_model(model_path=config.model_path)
    bentoml.pytorch.save_model('model_daflow', model)