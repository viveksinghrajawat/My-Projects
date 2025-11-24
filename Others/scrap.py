import requests
import requests
from bs4 import BeautifulSoup
  
URL = "https://testbook.com/objective-questions/mcq-on-python--5eea6a1139140f30f369ebae"
r = requests.get(URL)
  
soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
body=soup.find('div', attrs = {'class':'pure-g pure-u-1 pure-u-md-19-24 pure-u-lg-19-24 pure-u-xl-16-24'})
data=body.findAll('div',attrs={'class':'question-container'})
for i in data:
    ques=i.findAll('p')
    [print(k.text) for k in list(ques)]  
    opt=list(i.find('ol',attrs={'class':'options-list'}))
    for j in range(len(opt)):
        print(j+1,":",opt[j].text)
    # print(list(opt))
    ans=i.find('div',attrs={'class':'card answer-card'})
    print(ans.text)
    
    print("***********************")