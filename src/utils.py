import yaml
import pandas as pd

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def save_to_excel(data, file_path):
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)