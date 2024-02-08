#!/usr/bin/env python3.11

import scrapy
from scrapy.selector import Selector
from icecream import ic
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ScheduleSpider(scrapy.Spider):
    name = 'schedule_with_selenium_firefox'
    start_urls = ['https://uclabruins.com/sports/womens-beach-volleyball/schedule/2024']

    def __init__(self):
        opts = Options()
        #opts.add_argument("--headless") 
        opts.add_argument('--no-proxy-server')
        self.driver = webdriver.Firefox(options=opts)
        #self.driver = webdriver.Chrome(options=chrome_options)  # chrome

    def parse(self, response):
        self.driver.get(response.url)

        '''
        try:
            WebDriverWait(driver, 60).until(
                lambda d: d.execute_script('return document.readyState') == 'complete')
        except TimeoutException:
            self.logger.warning("Page load timed out but continuing with the data available.")
        '''

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.s-game-card'))
        )

        sel = Selector(text=self.driver.page_source)
        ic(len(sel.css('div.s-game-card')))
        for game in sel.css('div.s-game-card'):
            item = {}
            item['date'] = game.css('div.s-game-card__header__date span::text').get().strip()
            try:
                item['school'] = game.css(
                    'div.s-game-card__header__team a:nth-child(2)::text').get().strip()
            except Exception:
                item['school'] = game.css(
                    'div.s-game-card__header__team a:nth-child(2)::text').get().strip()
            #item['time'] = game.css('div.s-game-card__header__time span::text').get().strip()
            yield item
        
        self.driver.quit()
