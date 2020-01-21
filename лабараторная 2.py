import requests
from bs4 import BeautifulSoup as bs
import time
import datetime

#После работы программа сохранит все нужные статьи в папке

headers = {'accept': '*/*',
          'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
base_url = 'https://www.breitbart.com/politics/'
download_folder = '/links/'
stop_words= ['Democrat', 'Republican', 'GOP']

def check_list(text):
    for el in stop_words:
        if el in text:
            return True
        else:
            pass
    return False

def r_parse(base_url, headers,times):
    articles = []
    all_titles = []
    session = requests.session()
    # 15 часов - это разница между часовым поясом сайта (Pacific time) и местным (GMT+7)
    start_time = datetime.datetime.now() - datetime.timedelta(hours=15)
    for i in range(times):
        request = session.get(base_url, headers=headers)
        if request.status_code == 200:
            soup = bs(request.content, 'html.parser')
            divs = soup.find_all('div',class_= 'tC')
            for div in divs:
                post_time = datetime.datetime.strptime(div.find('footer').find('time').text[:-4], '%d %b %Y, %I:%M %p')
                title = div.find('a')['title']
                text = div.find('div',class_= 'excerpt').text
                author = div.find('footer').find('a').text
                link ='https://www.breitbart.com' + div.find('a')['href']
                if (start_time < post_time) and (title not in all_titles) and (check_list(title) or check_list(text)):
                    articles.append({'title': title,
                                 'text': text,
                                 'link' : link,
                                 'author': author,
                                 'post_time': post_time})

                    f = open('links/' + str(title).replace(' ', '_').translate({ord(i): None for i in '“”\/*?<>|:'})[:50] +'.html', 'wb')
                    f.write(requests.get(link).content)
                    f.close
                    all_titles.append(articles)
        print('hour number: ',i)
        time.sleep(60*60)
    else:
        print('thats all')
    return all_titles

day_articles = r_parse(base_url, headers,24)
print(day_articles)
