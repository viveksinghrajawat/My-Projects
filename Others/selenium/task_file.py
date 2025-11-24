import os
import re
import requests,csv
from bs4 import BeautifulSoup
  
URL = "https://www.snapdeal.com/products/mens-footwear-sports-shoes?sort=plrty"
r = requests.get(URL)
  
soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
alldata=soup.body.find_all('div',attrs={'class':'product-desc-rating'})

with open('datanew.csv', 'w') as datacsv:
        writ=csv.DictWriter(datacsv, fieldnames = ["Name","orignal_price", "snapdeal_price", "discount"])
        writ.writeheader()
for j in alldata:
    row=[]
    name_pro=j.find('p',attrs={'class':'product-title'})
    orignal_price=j.find('span',attrs={'class':'lfloat product-desc-price strike'})
    snapdeal_price=j.find('span',attrs={'class':'lfloat product-price'})
    dis=j.find('div',attrs={'class':'product-discount'})
    row.append(name_pro.text)
    row.append(str(orignal_price.text).strip())
    row.append(snapdeal_price.text)
    row.append(str(dis.text).strip())
    
    with open('datanew.csv', 'a+') as datacsv:
        writ=csv.writer(datacsv)
        writ.writerow(row)


def task():
    os.system('clear')
    Brand=["ASIAN","FITMonkey","UrbanMark","Campus","JQR","Impakto"]
    print("Brands Available in store")
    print(Brand)
    serch_name=input("Enter name  :")
    flag=0
    for  B_name in Brand:
        if B_name.lower()==serch_name.lower():
            flag=1
            with  open('datanew.csv', mode ='r') as f:
                        read=csv.DictReader(f)
                        for i in read:
                            result=re.match(B_name,i.get('Name'))
                            if result != None:
                                print(f"\nNAME           :{i.get('Name')}")
                                print(f"Orignal Price  :{i.get('orignal_price')}")
                                print(f"Snapdeal Price :{i.get('snapdeal_price')}")
                                print(f"Discount       :{i.get('discount')}")
    if flag==0:     
        print("wrong choice")
        task()
    else:
        ex=input("\npress 1 to reload or press any key to go back")
        if ex=='1':
            task()
        else:
            task_fun()

def discount_fun():
    os.system('clear')
    try:
        val=int(input("Enter discount"))
        print("\n1.less than \n2.more than \n3.Back")
        ch=input()
        if ch=='1':
            with  open('datanew.csv', mode ='r') as f:
                read=csv.DictReader(f)
                flag=0
                for i in read:
                    pr= ''.join(x for x in (i.get('discount')) if x.isdigit())
                    if int(pr) < val:
                        flag=1
                        print(f"\nNAME           :{i.get('Name')}")
                        print(f"Orignal Price  :{i.get('orignal_price')}")
                        print(f"Snapdeal Price :{i.get('snapdeal_price')}")
                        print(f"Discount       :{i.get('discount')}")
                if flag==0:
                    print("No data found")
                ex=input("\npress 1 to reload or press any key to go back")
                if ex=='1':
                    discount_fun()
                else:
                    task_fun()
        elif ch=='2':
            with  open('datanew.csv', mode ='r') as f:
                read=csv.DictReader(f)
                flag=0
                for i in read:
                    pr= ''.join(x for x in (i.get('discount')) if x.isdigit())
                    if int(pr) > val:
                        flag=1
                        print(f"\nNAME           :{i.get('Name')}")
                        print(f"Orignal Price  :{i.get('orignal_price')}")
                        print(f"Snapdeal Price :{i.get('snapdeal_price')}")
                        print(f"Discount       :{i.get('discount')}")
                if flag==0:
                    print("No data found")
                ex=input("\npress 1 to reload or press any key to go back")
                if ex=='1':
                    discount_fun()
                else:
                    task_fun()
        elif ch=='3':
            task_fun()
        else:
            print("wrong choice")
            discount_fun()
    except ValueError:
        print("wrong input")
        discount_fun()

def price():
    os.system('clear')
    try:
        val_st=int(input("Enter starting Price   :"))
        val_end=int(input("Enter ending Price     :"))
        
        with  open('datanew.csv', mode ='r') as file:
            read=csv.DictReader(file)
            flag=0
            for i in read:
                pr= ''.join(x for x in (i.get('snapdeal_price')) if x.isdigit())
                if int(pr) > val_st and int(pr)<val_end :
                    flag=1
                    print(f"\nNAME           :{i.get('Name')}")
                    print(f"Orignal Price  :{i.get('orignal_price')}")
                    print(f"Snapdeal Price :{i.get('snapdeal_price')}")
                    print(f"Discount       :{i.get('discount')}")
            if flag==0:
                print("No data found")
            ex=input("\npress 1 to reload or press any key to go back")
            if ex=='1':
                price()
            else:
                task_fun()
    except ValueError:
        print("wrong input")
        price()

def task_fun():
    os.system('clear')
    ch=input("search shoes by \n1.Name \n2.Price \n3.discount\n4.exit\n")
    if ch=='1':
        task()
    elif ch=='2':
        price()
    elif ch=='3':
        discount_fun()
    elif ch=='4':
        exit()
    else:
        print("wrong choice")
        task_fun()

task_fun()