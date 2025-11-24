import requests
import json
from datetime import date
import csv

result = requests.get("https://fakestoreapi.com/products")
data = result.text
parse_json = json.loads(data)
today = date.today()

cat_data = []
for i in parse_json:
    if i['category'] not in cat_data:
        cat_data.append(i['category'])
    else:
        pass

print(cat_data)    
category = input("enter your category for which you want data : ")
if category not in cat_data:
    print("Please enter correct category")
    category = input("enter your category for which you want data : ")
for i in parse_json:
    if i['category'] == category:
        f_name = (f"{category}_"+str(today))
        with open(f_name+'.csv',"w+")as f:
            # import pdb;pdb.set_trace()
            writ = csv.DictWriter(f, fieldnames= ['id','title', 'price', 'description','category','image','rate','count'])
            writ.writeheader()
        for i in parse_json:
            row = []
            if i['category'] == category:
                row.append(i['id'])
                row.append(i['title'])
                row.append(i['price'])
                row.append(i['description']) 
                row.append(i['category'])
                row.append(i['image'])
                row.append(i['rating']['rate'])
                row.append(i['rating']['count'])
                with open(f_name+'.csv','a+') as f1:
                    writ = csv.writer(f1)
                    writ.writerow(row)
        print("Your data sucessfully saved !!")
        break
        
  