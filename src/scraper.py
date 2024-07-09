from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

from src.exceptions.scrap_exceptions import ScrapNewsCaptchaCatch
from src.utils import contains_money,verifyDateLimit

from time import sleep
import logging
import random

class NewsScraper:
    def __init__(self, log: logging):
        self.log = log

    def scrape_news(self, phrase:str, category:str, months:datetime):

            browser = webdriver.Chrome()

            browser.get("https://www.reuters.com/")
            sleep(random.uniform(2, 5))
            if(browser.find_element(By.XPATH, '/html/body/iframe')):
                self.log.error("Captcha has been captured from website")
                raise ScrapNewsCaptchaCatch("Captcha has been captured from website")
            
            search_button = browser.find_element(By.XPATH, '/html/body/div[2]/header/div/div/div/div/div[3]/div[1]/button/span/svg')
            search_button.click()
            sleep(random.uniform(1, 3))
            search_input = browser.find_element(By.XPATH, '/html/body/div[2]/header/div/div/div/div/div[3]/div[1]/div/div')
            
            search_input.send_keys(phrase)
            sleep(random.uniform(1, 2))
            search_input.send_keys(Keys.RETURN)

            WebDriverWait(browser, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "search-results"))
            )

            articles = browser.find_elements(By.XPATH, '//*[@id="fusion-app"]/div[2]/div[2]/div/div[2]/div[2]/ul')
            sleep(random.uniform(1, 5))
            
            for article in articles:
                title = article.find_element(By.XPATH, '//*[@id="fusion-app"]/div[2]/div[2]/div/div[2]/div[2]/ul/li[1]/div/div/header/a/span').text
                date_str = article.find_element(By.XPATH, '//*[@id="fusion-app"]/div[2]/div[2]/div/div[2]/div[2]/ul/li[1]/div/div/time').text

                image_element = article.find_element(By.XPATH, '//*[@id="fusion-app"]/div[2]/div[2]/div/div[2]/div[2]/ul/li[1]/div/a/div/div[1]/div/img')
                image_url = image_element.get_attribute('src')
                
                if verifyDateLimit(limitDate=months,dateScrap=date_str):
                    search_count = title.lower().count(phrase.lower()) + description.lower().count(phrase.lower())
                    contains_money = contains_money(title) or contains_money(description)
                    news_data.append({
                        'title': title,
                        'date': date,
                        'description': description,
                        'picture_filename': "",  # Ajustar se necessário
                        'search_count': search_count,
                        'contains_money': contains_money
                    })

            browser.quit()
            return news_data



    
