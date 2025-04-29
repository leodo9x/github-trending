import requests
from bs4 import BeautifulSoup

def get_url(date = ''):
    url = 'https://github.com/trending'

    if date:
        url = f'{url}?since={date}'

    return url

def get_github_trending(article):
    title = article.h2
    link = f"github.com{title.a.get('href')}"
    name = title.a.text.split()[-1]

    description = ""
    if article.p:
        description = article.p.text.replace('\n', '').strip()

    language = None
    if article.find('span', itemprop="programmingLanguage"):
        language = article.find('span', itemprop="programmingLanguage").text

    star = article.find('a', class_="Link--muted").text.strip()

    return {
        "name": name,
        "link": link,
        "description": description,
        "language": language,
        "star": star
    }

def init(date = ''):
    url = get_url(date)

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    return list(map(get_github_trending, soup.find_all('article')))