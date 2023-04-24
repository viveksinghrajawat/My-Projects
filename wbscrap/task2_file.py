import os,csv
def display(i):
    os.system('clear')
    print("******Snapdeal Shoes Store*****")
    print(f"\nNAME           :{i.get('Name')}")
    print(f"Orignal Price  :{i.get('orignal_price')}")
    print(f"Snapdeal Price :{i.get('snapdeal_price')}")
    print(f"Discount       :{i.get('discount')}")


def check():
    u_in=input("\nPrivious(p/P)   Exit(e/E)   Next(n/N)\n")
    if u_in.lower()=='p':
        return 'p'
    elif u_in.lower()=='e':
        exit()
    elif u_in.lower()=='n' :
        return 'n'
    else:
        check()                    

def prev(k):
    with  open('datanew.csv', mode ='r') as file:
        read=csv.DictReader(file)
        for j, line in enumerate(read):
            if j==k-1 and k>0:
                display(line)
                n=check()
                return n

def nextdet(m):
    with  open('datanew.csv', mode ='r') as file:
        read=csv.DictReader(file)
        for j, line in enumerate(read):
            if j==m+1 and m<row_count:
                display(line)
                n=check()
                return n


def cal_len():
    with  open('datanew.csv', mode ='r') as file:
        read=csv.DictReader(file)
        data = list(read)
        row_count = len(data)
        return row_count

with  open('datanew.csv', mode ='r') as file:
    read=csv.DictReader(file)
    row_count = cal_len()
    for num, line in enumerate(read):
        display(line)
        d=check()
        if d=='p':
            if num>0:
                number=num-1
                while(number<num ):
                    if number==num:
                        break
                    else:
                        d=prev(number)
                        if d=='p':
                            number-=1
                        else:
                            number+=1
            if num==0:
                while(num==0):
                    display(line)
                    d=check()
                    if d=='p':
                        pass
                    else:
                        num+=1

        if d=='n':
            if num<row_count:
                number=num+1
                while(number>num):
                    if number==num:
                        break
                    else:
                        d=nextdet(number)
                        if d=='n':
                            number+=1
                        else:
                            number-=1
            else:
                display(line)
       
        
            
            
                


                