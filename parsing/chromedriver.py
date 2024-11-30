from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.webdriver.common.by import By

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
filter = "По времени"

find = "Парсинг на python"
urlpath= f'https://habr.com/ru/search/?q={find}&target_type=posts&order=relevance'
driver.get(urlpath)
tpa = []
sleep(15)
count_post = 5
def filter_set():
    filter = "По релевантности" # Выбираем фильтр
    if filter == "По релевантности":
        filter_change = driver.find_element("xpath", '//*[text()="по релевантности "]')
        filter_change.click()
    elif filter == "По времени":
        filter_change = driver.find_element("xpath", '//*[text()="по времени "]')
        filter_change.click()
    elif filter == "По рейтингу":
        filter_change = driver.find_element("xpath", '//*[text()="по рейтингу "]')
        filter_change.click()
    else:
        print("Такого фильтра нет")

    sleep(5)

for i in range(1, count_post+1):
    title = driver.find_element("xpath", f'(//a[@class="tm-title__link"])[{i}]/span')
    text_p = driver.find_element("xpath", f'(//div[@class="article-formatted-body article-formatted-body article-formatted-body_version-2"])[{i}]/p')
    a_href = driver.find_element("xpath", f'((//a[@class="tm-title__link"]){[i]})').get_attribute("href")
    if filter == "По времени":
        time = a_href = driver.find_element("xpath", f'(//time)[{i}]')
        tpa.append([title.text, text_p.text, a_href, time])
    else:
        tpa.append([title.text, text_p.text, a_href])
    
print(tpa)

sleep(3)
   
