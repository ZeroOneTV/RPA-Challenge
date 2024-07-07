from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import re
import os
import logging

class NewsScraper:
    def __init__(self, config):
        self.config = config
        self.news_data = []
        self.browser = webdriver.Chrome()  # ou qualquer outro driver compatível

    def scrape_news(self):
        search_phrase = self.config['robocloud']['workitem']['search_phrase']
        category = self.config['robocloud']['workitem']['category']
        months = self.config['robocloud']['workitem']['months']
        date_limit = datetime.now() - timedelta(days=30*months)

        self.browser.get("https://www.reuters.com/")
        search_input = self.browser.find_element(By.NAME, "search-field")
        search_input.send_keys(search_phrase)
        search_input.send_keys(Keys.RETURN)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-results"))
        )

        articles = self.browser.find_elements(By.CSS_SELECTOR, "article.story")
        for article in articles:
            title = article.find_element(By.CSS_SELECTOR, "h3").text
            date_str = article.find_element(By.CSS_SELECTOR, "time").get_attribute("datetime")
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            description = article.find_element(By.CSS_SELECTOR, "p").text if article.find_elements(By.CSS_SELECTOR, "p") else ""
            if(date >= date_limit):
                search_count = title.lower().count(search_phrase.lower()) + description.lower().count(search_phrase.lower())
                contains_money = self.contains_money(title) or self.contains_money(description)
                self.news_data.append({
                    'title': title,
                    'date': date,
                    'description': description,
                    'picture_filename': "",  # Ajustar se necessário
                    'search_count': search_count,
                    'contains_money': contains_money
                })

        self.browser.quit()
        return self.news_data

    def contains_money(self, text):
        pattern = r'\$?\d+([\.,]?\d+)?(\s?(USD|dollars))?'
        return bool(re.search(pattern, text))
