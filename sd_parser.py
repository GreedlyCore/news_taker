from bs4 import BeautifulSoup
import requests as rq
import re
from fake_headers import Headers
from random import randint, shuffle, choice
from telegraph import Telegraph
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime

header = Headers(
    browser="chrome",  # Generate only Chrome UA
    os="win",  # Generate ony Windows platform
    headers=True  # generate misc headers
)

# returns a url to auto generated article special for PC
def get_telegraph(article):  # images=None
    telegraph = Telegraph()
    while True:
        try:
            telegraph.create_account(short_name='UNTITLED')
        except:
            print('cant create account for telegraph')
        else:
            break
        #prevents error
        sleep(5)
    #sub tag isnt allowed
    article['text'] = article['text'].replace('<sub>', '').replace('</sub>', '')
    content = f"<p>Date: {article['date']}</p><p>Source: {article['source']}\n</p><p>Summary: {article['summary']}</p>" + \
              article['text']

    response = telegraph.create_page(
        "article",

        html_content=content
    )
    return f"https://telegra.ph/{response['path']}"

#--------------------------------------GET----------------URL#--------------------------------------#------------------#

# returns a url of random themed article
def get_url(theme):
    headers = header.generate()

    root = "https://www.sciencedaily.com/news/" + theme
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get(root)
    btn = driver.find_element_by_id('load_more_stories')
    btn.click()
    sleep(1)

    soup = BeautifulSoup(driver.execute_script("return document.documentElement.outerHTML;"), 'html.parser')
    driver.close()
    urls = ["https://www.sciencedaily.com" + item.find('a', href=True)['href'] for item in
            soup.find('div', class_="tab-content").find_all('h3', class_="latest-head")]
    # содержит в себе элементы, а возвращается NoneType в выводе снизу также нон тайп

    if type(urls) == None:
        raise Exception()
    return urls

# returns a top article urls
def get_top_url():
    headers = header.generate()
    root = "https://www.sciencedaily.com/news/top/"

    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get(root)
    btn = driver.find_element_by_id('load_more_stories')
    btn.click()
    sleep(1)

    soup = BeautifulSoup(driver.execute_script("return document.documentElement.outerHTML;"), 'html.parser')
    url = []

    for item in soup.find('div', class_='col-md-8 col-md-push-4').find('div', class_="right-tabs clearfix").find(
            'div', class_="tab-content").find_all('h3',
                                                  class_="latest-head"):  # .find_all('div',class_="row"):  # , limit=count):
        link = "https://www.sciencedaily.com" + item.find('a', href=True)['href']
        url.append(link)

    driver.close()
    return  url


#--------------------------------------GET-SOMETHING-FROM-URL#--------------------------------------#------------------#

# returns a text of article by paraghraphs
def get_content(site, headers):
    soup_article = BeautifulSoup(rq.get(site, headers=headers).text, 'html.parser')
    lst = soup_article.find('div', {"id": "story_text"}).find('div', {"id": "text"}).find_all('p')
    lst = list(map(lambda x: str(x), lst))
    return ''.join(lst)


def get_description(site, headers):
    soup_article = BeautifulSoup(rq.get(site, headers=headers).text, 'html.parser')
    data = [soup_article.find('dl', class_="dl-horizontal dl-custom").find('dd', {"id": "date_posted"}).get_text(
        strip=True),
        soup_article.find('dl', class_="dl-horizontal dl-custom").find('dd', {"id": "source"}).get_text(strip=True),
        soup_article.find('dl', class_="dl-horizontal dl-custom").find('dd', {"id": "abstract"}).get_text(
            strip=True)]

    return dict(zip(['date', "source", "summary"], data))


def get_related_themes(site, headers):
    themes = {}
    main_themes = []
    soup_themes = BeautifulSoup(rq.get(site, headers=headers).text, 'html.parser')

    arr = [i.get_text(strip=True) for i in soup_themes.find('ul', {"id": "related_topics"}).find_all('a')]
    if len(main_themes) > 1:
        for i in range(len(main_themes)):
            try:
                wall = [arr.index(main_themes[i]), arr.index(main_themes[i + 1])]
            except:
                themes.update({main_themes[i]: arr[arr.index(main_themes[i]) + 1:]})
                break
            themes.update({main_themes[i]: arr[wall[0] + 1:wall[1]]})
    else:
        themes.update({arr[0]: arr[1:]})

    return themes


def get_name(site, headers):
    soup_name = BeautifulSoup(rq.get(site, headers=headers).text, 'html.parser')
    return soup_name.find('div', "col-sm-8 main less-padding-right hyphenate").find('h1', {"id": "headline"},
                                                                                    class_='headline').get_text(
        strip=True)


def article(site):
    headers = header.generate()
    desc = get_description(site, headers)
    article = {
        "name": get_name(site, headers),
        "themes": get_related_themes(site, headers),
        'date': desc['date'],
        "source": desc['source'],
        "summary":desc['summary'],
        "url": site,
        "text": get_content(site, headers),
    }
    return article
