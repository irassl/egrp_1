from selenium import webdriver
from mydatabase import *
from sqlalchemy.orm import sessionmaker
import re
import time
import os
import pandas


class Egrp365:
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
        self.save_parse(params)

    def save_parse(self, params):
        # try/exept
        table = self.driver.find_elements_by_id("mapFlyout")
        table_flat = self.driver.find_elements_by_id("information_about_object")

        if len(table) > 0:
            div_talbe = self.driver.find_element_by_css_selector("div.table")
            self.parse_re1(div_talbe)

        elif len(table_flat) > 0:
            div_infor = self.driver.find_element_by_css_selector(
                "div#information_about_object"
            )
            div_infor = list(filter(None, div_infor.text.split("\n")))
            self.parse_re(div_infor)
        else:
            querry = Address(
                address=params,
                kadastor=None,
                descrip=None,
                flar=None,
                okato=None,
                type_f=None,
                link=None,
            )
            self.querry_commit(querry)

    def querry_commit(self, querry):
        self.Session = sessionmaker()
        self.Session.configure(bind=engine)
        self.session = self.Session()
        try:
            self.session.add(querry)
            self.session.commit()
        except:
            print("no add")
        time.sleep(2)
        # self.driver.quit()

    def parse_re(self, div_infor):

        param = []
        for i in div_infor:
            param.append(re.search("\w+ — (?P<param>.+)", i).group("param"))

        kadastor, _, descrip, floar, area, address = param
        flar = str(floar + " " + area)
        print(param)
        querry = Address(
            address=address,
            kadastor=kadastor,
            descrip=descrip,
            flar=flar,
            okato=None,
            type_f=None,
            link=None,
        )
        self.querry_commit(querry)

    def parse_re1(self, div_talbe):
        table = div_talbe.text.split("\n")
        _, address, okato, _, kadastor, *rest = table[1::2]
        ##apFlyout > ul > li:nth-child(9) > a
        link = div_talbe.find_element_by_css_selector(
            "li:nth-child(9) > a"
        ).get_attribute("href")
        querry = Address(
            address=address,
            kadastor=kadastor,
            descrip=None,
            flar=None,
            okato=okato,
            type_f=None,
            link=link,
        )
        self.querry_commit(querry)


if __name__ in "__main__":

    # parsh = Egrp365(params="Москва ул Кутузова, д 1")
    # pars = Egrp365(params="129327, Москва г, , ул. Чичерина, д. 2/9, кв. 33")
    # pars.save_parse()
    # г Щербинка, ул Кутузова, д. 1, 1
    xml = pandas.read_excel("testxml.xlsx")
    values = xml["Adress"].values

    egrp = Egrp365(param=values[1:5])

