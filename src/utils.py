import yaml
import pandas as pd
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests

from src.exceptions.scrap_exceptions import ScrapNewsDownloadImageError

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

def contains_money(text: str) -> bool:
    pattern = r'\$?\d+([\.,]?\d+)?(\s?(USD|dollars))?'
    return bool(re.search(pattern, text))

def verifyMonthData(data) -> datetime:
    if isinstance(data, str):
        try:
            data = int(data)
        except ValueError:
            raise ValueError("The provided string cannot be converted to an integer.")
    elif not isinstance(data, int):
        raise TypeError("The provided data type is not supported. It must be a string or an integer.")

    if data < 0:
        raise ValueError("The provided number must be zero or a positive integer.")

    current_date = datetime.now()

    start_date = current_date - relativedelta(months=data-1) if data > 0 else current_date

    return start_date

def verifyDateLimit(limitDate:datetime, dateScrap:str) -> bool:
    # Converte a data de scrape (string) para datetime
    try:
        date_scrap = datetime.strptime(dateScrap, "%B %d, %Y")
    except ValueError:
        raise ValueError("The provided dateScrap is not in the correct format 'July 3, 2024'.")

    if (date_scrap >= limitDate):
        return True
    else:
        return False
    
def downloadImagemFromArticle(urlBase:str,nameFile:str):
    try:
        image_response = requests.get(urlBase)
        image_filename = f"{nameFile}.jpg"
        with open('./output/images/'+image_filename, 'wb') as file:
            file.write(image_response.content)
        file.close()
    except Exception:
        raise ScrapNewsDownloadImageError("")