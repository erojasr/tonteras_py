import requests
from bs4 import BeautifulSoup
    

res = requests.get('https://news.ycombinator.com/news?p=15')

#print(res.text)

soup = BeautifulSoup(res.text, 'html.parser')
print(soup.select('.athing'))
#print(soup.body.contents)
#print(soup.find_all('a'))
#print(soup.find(id='score_20514755'))
#print(soup.select('.score'))

links = soup.select('.storylink')
#votes = soup.select('.score')
subtext = soup.select('.subtext')

#print(votes[0])
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
#print(xd)