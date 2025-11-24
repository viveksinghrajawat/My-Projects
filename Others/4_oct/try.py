import requests
import bs4
  
URL = "https://buildmedia.readthedocs.org/media/"
r = requests.get(URL)
  
soup = bs4(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
print(soup.prettify())