import re,csv
def testt():
    with open("ans.csv") as f:
        obj3=csv.reader(f)
        for i in obj3:
            flag=[]
            for m in i:
                pt1= re.match('\[+[A-D]+\]+\.+.',m)
                if pt1==None:

                    pt2=re.match('.+\]+\.+.',m)
                    pt3=re.match('\[+[A-D]+\.+',m)
                    if pt2!=None or pt3!=None:
                        flag.append("1")
                    else:
                        flag.append("2")
                else:
                    flag.append("0")
            if '0' in flag:
                if '1' in flag:
                    return -1
                else:
                    pass
            else:
                return -1
