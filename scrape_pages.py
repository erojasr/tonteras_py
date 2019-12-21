import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup

page = 1
url = 'https://news.ycombinator.com/news'
links = []
subtext = []
while True:

    try:
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        if page == 1:
            res = session.get(url)
        else:
            print(url+'?p='+str(page))
            res = session.get(url+'?p='+str(page))
    except requests.exceptions.ConnectionError as error:
        print(error.response)
        break
        

    soup = BeautifulSoup(res.text, 'html.parser')

    # validate when page empty data
    # if page empty break while
    #print(soup.select('.athing'))
    content = soup.select('.athing')
    if not content:
        break

    links.append(soup.select('.storylink'))
    subtext.append(soup.select('.subtext'))

    #print(len(links))

    page += 1
else:
    print('done reading pages')



#print(links)

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key= lambda k:k['votes'], reverse=True)

def create_custom_hn(links, subtext):
    hn = [] # new list hacker news
    for index, item in enumerate(links):
        title = links[index].getText()
        href = links[index].get('href', None)
        vote = subtext[index].select('.score')
        points = 0
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
        hn.append({'title': title, 'link': href, 'votes': points})

    return sort_stories_by_votes(hn)


xd = create_custom_hn(links, subtext)
print(xd)