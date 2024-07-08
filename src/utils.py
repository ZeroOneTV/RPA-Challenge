import yaml
import pandas as pd

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def save_to_excel(data, file_path):
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)

def category_exist(data: str) -> bool:
    categories = {
        "All": True,
        "World": True,
        "Business": True,
        "Legal": True,
        "Markets": True,
        "Breakingviews": True,
        "Technology": True,
        "Sustainability": True,
        "Science": True,
        "Sports": True,
        "Lifestyle": True,
    }
    return data in categories