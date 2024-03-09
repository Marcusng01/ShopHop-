from re import search
import os
import sys
from typing import overload
from bs4 import BeautifulSoup
from multiprocessing import freeze_support
freeze_support()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep
import undetected_chromedriver as uc
import random, threading, webbrowser


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def is_float(element):
    try:
        float(element)
        return True
    except ValueError:
        return False

def shoppee(search):
    chrome_options = webdriver.ChromeOptions()
    base_url = 'https://shopee.com.my/search?keyword=' + search
    chrome_options.add_argument('disable-notifications')
    chrome_options.add_argument('start-maximized')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 2
        })
    browser = webdriver.Chrome(resource_path('./driver/chromedriver.exe'), chrome_options=chrome_options, service=Service(ChromeDriverManager().install()))
    browser.get(base_url)
    delay = 5 #secods

    WebDriverWait(browser, delay)
    print ("Page is ready")
    sleep(5)
    html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    browser.quit()
    soup = BeautifulSoup(html, "lxml")
    items = soup.find_all('div',class_='col-xs-2-4 shopee-search-item-result__item')
    num_results = 5
    s_list=[]
    for i in range(num_results):
        item = items[i]    
        
        temp = item.find('img')
        if temp.has_attr('src'):
            image = temp['src']
        if temp.has_attr('alt'):    
            name = temp['alt']

        spans = item.find_all('span')
        for text in spans:
            text = text.text
            if is_float(text):
                price = "RM" + text

        link = "https://shopee.com.my/" + item.find('a')['href']   
        #print(f"Item {counter}. \nName: {name} \nLink: {link}\n")
        item = [image,name,price,link]
        s_list.append(item)
        
    return s_list

def lazada(search):
    chrome_options = webdriver.ChromeOptions()
    base_url = 'https://www.lazada.com.my/catalog/?q=' + search
    chrome_options.add_argument('disable-notifications')
    chrome_options.add_argument('start-maximized')
    browser = uc.Chrome(executable_path=resource_path('./driver/chromedriver.exe'),chrome_options=chrome_options, service=Service(ChromeDriverManager().install()))
    browser.get(base_url)
    delay = 5 #secods

    WebDriverWait(browser, delay)
    print ("Page is ready")
    sleep(5)
    html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    browser.quit()
    soup = BeautifulSoup(html, "lxml")
    items = soup.find_all('div',class_='Bm3ON')
    num_results = 5
    s_list=[]
    for i in range(num_results):
        item = items[i]      
        name = item.find('img')['alt']
        image = item.find('img')
        if image.has_attr('src'):
            image = image['src']
        span = item.find('span').text

        link = item.find('a')['href']   
        item = [image,name,span,link]
        s_list.append(item)

    return s_list

def wowshop(search):
    chrome_options = Options()
    base_url = 'https://www.wowshop.com.my/catalogsearch/result/?q=' + search
    chrome_options.add_argument('disable-notifications')
    chrome_options.add_argument('start-maximized')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 2
        })
    browser = webdriver.Chrome(resource_path('./driver/chromedriver.exe'), chrome_options=chrome_options, service=Service(ChromeDriverManager().install()))
    browser.get(base_url)
    delay = 5 #secods

    WebDriverWait(browser, delay)
    print ("Page is ready")
    sleep(5)
    html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    browser.quit()
    soup = BeautifulSoup(html, "lxml")
    items = soup.find_all('li',class_='item product product-item col-3')
    num_results = 5
    s_list=[]
    for i in range(num_results):
        item = items[i]    
        link = item.find('a')['href']   
        name = item.find('img')['alt']
        image = item.find('img')
        if image.has_attr('src'):
            image = image['src']
        span = item.find('span',class_ = 'price').text

        link = item.find('a')['href']   
        item = [image,name,span,link]
        s_list.append(item)

    return s_list


# importing Flask and other modules
from flask import Flask, request, render_template 

# Flask constructor
app = Flask(__name__)   


# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
        search = request.form.get("search")


        overall =[lazada(search),shoppee(search),wowshop(search)]

        return render_template("Moschino _ Minimalist Free HTML Portfolio by WowThemes.net.html", content = overall)

    return render_template("form.html")

if __name__ == '__main__':
    port = 5000
    url = "http://127.0.0.1:{0}".format(port)

    threading.Timer(1.25, lambda: webbrowser.open(url) ).start()

    app.run(debug=False, use_reloader=False, port = port)
