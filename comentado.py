import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import tabulate
import pandas as pd
import itertools
page = 1
url = 'https://news.ycombinator.com/news'
links = []
subtext = []
data = []
votes = []
titles = []
while True:

    try:
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        if page == 1:
            print(url)
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
    
    #links.append([x.get('href') for x in soup.select('.storylink')])
    #votes.append([int(link.find('span', class_='score').getText().replace(' points','')) if link.find('span', class_='score') else 0 for link in soup.select('.subtext')])
    #titles.append([z.getText() for z in soup.select('.storylink')])
  
    links  += [x.get('href') for x in soup.select('.storylink')]    
    votes  += [int(link.find('span',class_='score').getText().replace(' points','')) if link.find('span', class_='score') else 0 for link in soup.select('.subtext')]
    titles += [z.getText() for z in soup.select('.storylink')]
    #[y.getText().replace(' points','') if len(y) else 0 for y in soup.select('.score')]
    

    #for y in soup.select('.score'):
    #    if len(y):
    #        votes.append(y.getText().replace('points',''))
    #    else:
    #        votes.append(0)

    if page == 3:
       break

    #data.append({'links': soup.select('.storylink'), 'subtext': soup.select('.subtext')})

    #print(len(links))
    
    page += 1
else:
    print('done reading pages')


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key= lambda k:k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = [] # new list hacker news
    for index, item in enumerate(links):
        for idx, value in enumerate(item):
            title = item[idx].getText()
            href = item[idx].get('href', None)
            vote = subtext[index][idx].select('.score')
            points = 0
            if len(vote):
                points = int(vote[0].getText().replace(' points', ''))
            hn.append({'title': title, 'link': href, 'votes': points})
            #hn.append({'title': title, 'votes': points})

    return sort_stories_by_votes(hn)

#print([len(value) for a,value in enumerate(titles)])
#print([len(value) for a,value in enumerate(links)])
#print([len(value) for a,value in enumerate(votes)])
#print(titles[0])
#print(len(titles))
#print(len(links))
#print(len(votes))
#dataset = create_custom_hn(links, subtext)
#data = list(map(list.__add__,titles,links))

#data = titles+links+votes

#data = [a + b + c for a, b, c in zip(titles, links, votes)]
#dataframe = pd.DataFrame([list(itertools.chain(*i)) for i in zip(titles, zip(links, votes))], columns=['Title','Link','Votes'])
dataframe = pd.DataFrame(list(zip(titles,links,votes)), columns=['Title','Link','Votes'])
print(dataframe.sort_values(by='Votes', ascending = False))
#header = dataset[0].keys()
#
#print(header)
#rows = [article.values() for article in dataset]
#print(tabulate.tabulate(rows, header, tablefmt='grid'))

