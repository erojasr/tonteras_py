import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import pandas as pd

page = 1
url = 'https://news.ycombinator.com/news'
links, votes, titles = [],[],[]
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
  
    links  += [x.get('href') for x in soup.select('.storylink')]    
    votes  += [int(link.find('span',class_='score').getText().replace(' points','')) if link.find('span', class_='score') else 0 for link in soup.select('.subtext')]
    titles += [z.getText() for z in soup.select('.storylink')]


    #if page == 3:
    #   break
    
    page += 1

# displaying data
dataframe = pd.DataFrame(list(zip(titles,links,votes)), columns=['Title','Link','Votes'])
print(dataframe.sort_values(by='Votes', ascending = False))


