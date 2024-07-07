from src.scraper import NewsScraper
from src.utils import load_config, save_to_excel
from robocorp.tasks import task
from robocorp import workitems
from src.utils import load_config
import logging
import re

# Configuração de logging
logging.basicConfig(level=logging.INFO, filename='logs/app.log', 
                    format='%(asctime)s %(levelname)s:%(message)s')

@task
def carregar_config():
    return load_config('config/config.yaml')

@task
def carregar_work_item():
    work_item = []
    for item in workitems.inputs:
        work_item.append()
    search_phrase = work_item.payload.get("search_phrase")
    news_category = work_item.payload.get("news_category")
    months = work_item.payload.get("months")

    # Retorna os parâmetros como um dicionário
    return {
        "search_phrase": search_phrase,
        "news_category": news_category,
        "months": months
    }

@task
def raspar_noticias(params, config):
    scraper = NewsScraper(config)
    return scraper.scrape_news(params)

@task
def salvar_em_excel(news_data):
    save_to_excel(news_data, 'output/news_data.xlsx')

@task
def main():
    config = carregar_config()
    params = carregar_work_item()
    news_data = raspar_noticias(params, config)
    salvar_em_excel(news_data)
