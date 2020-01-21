import requests
from bs4 import BeautifulSoup as bs
from collections import deque
from tqdm import tqdm
import time
headers = {'accept': '*/*',
          'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

first_url =  'https://en.wikipedia.org/wiki/Special:Random'
second_url =  'https://en.wikipedia.org/wiki/Special:Random'


session = requests.session()

def get_url_page(page_url, headers):
    page = ''
    while page == '':
        try:
            page = requests.get(page_url, headers=headers)
            break
        except:
            print(request.status_code)
            print("Connection refused by the server..")
            time.sleep(15*60)
            continue

    #request = session.get(page_url)
    request = requests.get(page_url)
    time.sleep(3)
    wiki_url = []

    if request.status_code == 200:
        soup = bs(request.text, 'html.parser')
        p_text = soup.find_all('p')

        for p in p_text:
            for href in p.find_all('a'):
                try:
                    if 'wiki/' in href.get("href"):
                        wiki_url.append('https://en.wikipedia.org' + href.get("href"))
                except TypeError:
                    pass
        return list(set(wiki_url))

def get_path(first_url,second_url):
    queue = deque(get_url_page(first_url,headers=headers))
    distances = {url: 1 for url in queue}
    parents = {url: first_url for url in queue}
    while second_url not in distances and max(distances.values()) <=7:
        cur_url  = queue.popleft()
        new_url = get_url_page(cur_url,headers=headers)
        for u in tqdm(new_url):
            if u not in distances:
                print(new_url)
                queue.append(u)
                distances[u] =distances[cur_url] + 1
                parents[u] = cur_url
    path = [second_url]
    parent = parents[second_url]
    parents[first_url] = None
    while not parent is None:
        path.append(parent)
        parent = parents[parent]
    if max(distances.values()) >=7:
        return('no root')
    else:
        return(path)

print('Путь туда: ',get_path(first_url,second_url))
print('Путь обратно: ',get_path(second_url,first_url))

