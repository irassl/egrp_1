from selenium import webdriver
from mydatabase import *
from sqlalchemy.orm import sessionmaker
from scrapy.http import HtmlResponse

# from scrapy import Selector
from scrapy.selector import Selector
import re
import time
import os
import pandas


class Egrp365:
    # __slots__ = ['params']

    def __init__(self, params=None, param=None):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("--window-size=900,768")
        # sdelat' list i 4tobi mogno bilo ne vixodit' iz browers
        self.param = param
        self.params = params
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.implicitly_wait(5)

        if self.params is None:
            self.list_search(param)
        else:
            self.search(params)

    def list_search(self, param):

        for i in param:
            self.search(i)

    def search(self, params):
        self.driver.get("https://egrp365.ru/")
        search_elem = self.driver.find_element_by_id("address")
        search_elem.send_keys(params)
        time.sleep(1)
        search_el = self.driver.find_elements_by_class_name("suggestions-suggestions")
        new_search = search_el[0].text.split("\n")
        search_elem.clear()
        search_elem.send_keys(new_search[0])
        self.driver.find_element_by_id("search_by_kad_num").click()

        # if len(self.driver.find_elements_by_id("mapFlyout")) == 0:
        # self.driver.find_element_by_xpath(
        #  '//*[@id="result_search"]/div[2]/div[1]'
        #  ).click()
        list_search = self.driver.find_elements_by_css_selector(".rs_address a")
        for i in list_search:
            print(params)
            if (params.split(" ")[1] and params.split(" ")[-1]) in i.text:
                i.click()
            # elif params.split(" ")[1] in i.text:
            # i.click()
        # click = list_search.find_element_by_link_text("params").click()
        # time.sleep(3)
        # self.save_parse(params)
        self.parse_re(self.driver.current_url)
        print(self.driver.current_url)

    def save_parse(self, params=None):
        # try/exept
        table = self.driver.find_elements_by_id("mapFlyout")
        table_flat = self.driver.find_elements_by_id("information_about_object")

        if len(table) > 0:
            self.parse_text_house(table)
        elif len(table_flat) > 0:
            self.parse_text_flat(table_flat)
            # self.driver.quit()
        else:
            self.save_none(params)

    def querry_commit(self, querry):
        self.Session = sessionmaker()
        self.Session.configure(bind=engine)
        self.session = self.Session()
        try:
            self.session.add(querry)
            # self.session.commit()
        except:
            print("no add")
        # self.driver.quit()

    def save_none(self, params):
        querry = AddressNone(params)
        self.querry_commit(querry)

    def parse_text_house(self, table):
        tables = []
        for i in table:
            tables.extend(i.text.split("\n"))
        print(tables[:10])
        # OrderedDict
        dict_house = dict(zip(tables[2:17:2], tables[3:17:2]))
        querry = House(*dict_house.values())
        self.querry_commit(querry)
        # self.driver.quit()
        print(dict_house)

    def parse_text_flat(self, table_flat):
        tables = []
        for i in table_flat:
            tables.extend(i.text.split("\n"))
        tables = list(filter(None, tables))
        # table = [n.split("—") for n in tables]
        table = []
        for n in tables:
            table.extend(n.split("—"))
        print(table[:10])
        dict_flat = dict(zip(table[::2], table[1::2]))
        querry = Flat(*dict_flat.values())
        self.querry_commit(querry)
        # self.driver.quit()
        print(dict_flat)

    def parse_re(self, current_url):
        # scrapy
        regex = "(?P<address>\S+) \n (?P<okato>\S+) (?P<kadastr>\S+) "
        table = []
        # for i in tables:
        #   table.extend(i.text.split("\n"))

        # table = list(filter(None, table))
        self.response = HtmlResponse(url=current_url, body=body)
        self.sel = Selector(response=self.response)
        print(self.sel.xpath("//li/span/text()").getall())
        print(self.response.xpath("//title/text()").getall())


if __name__ in "__main__":

    # pars = Egrp365(params="Москва ул Кутузова, д 3 1")
    # pars = Egrp365(params='129327, Москва г, , ул. Чичерина, д. 2/9, кв. 233')
    # pars.save_parse()
    # г Щербинка, ул Кутузова, д. 1, 1
    xml = pandas.read_excel("testxml.xlsx")
    values = xml["Adress"].values

    egrp = Egrp365(param=values[4:5])

