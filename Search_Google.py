from better_profanity import profanity
import random
import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
from urllib.parse import urlparse
def search(query,type,limit,safe):
  def googleSearch():
          g_clean = []
          if safe:
            url =             'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(query)
          else:
            url='https://www.google.com/search?client=firefox-b-1-d&q={}&safe=images'.format(query)
          try:
            html = requests.get(url)
            if html.status_code==200:
                soup = BeautifulSoup(html.text, 'lxml')
                a = soup.find_all('a') 
                for i in a:
                    k = i.get('href')
                    try:
                        m = re.search("(?P<url>https?://[^\s]+)", k)
                        n = m.group(0)
                        rul = n.split('&')[0]
                        domain = urlparse(rul)
                        if(re.search('google.com', domain.netloc)):
                            continue
                        else:
                            g_clean.append(rul)
                    except:
                        continue
          except:
            print(str(Exception))
          finally:
            return g_clean
  y = 0
  final=''
  for result in googleSearch():
    if safe and profanity.contains_profanity(result) or safe and profanity.contains_profanity(query):
      final += ''
    else:
      if type == 'link':
        if not result[-3] + result[-2]  + result[-1] in ['jpeg','jpg','png','gif']:
          if y <= limit:
            final += result + '\n'
          y+=1
      else:
        if y <= limit:
          final += result + '\n'
        y+=1
  return final