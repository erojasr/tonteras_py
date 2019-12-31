import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import pandas as pd

page = 1
url = 'https://news.ycombinator.com/news'
links, votes, titles, ages = [], [], [], []
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
        print('We don\'t have more data to extract')
        break
  
    links  += [link.get('href') for link in soup.select('.storylink')]
    votes  += [int(points.find('span', class_='score').getText().replace(' points', '')) if points.find('span', class_='score') else 0 for points in soup.select('.subtext')]
    titles += [title.getText() for title in soup.select('.storylink')]
    ages   += [age.find('span', class_='age').getText().replace(' ago',"")  for age in soup.select('.subtext')]

    #if page == 3:
    #   break
    
    page += 1

# displaying data
dataframe = pd.DataFrame(list(zip(titles,links,votes, ages)), columns=['Title', 'Link', 'Votes', 'Age'])
print(dataframe.sort_values(by='Votes', ascending=False))


