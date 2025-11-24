import csv,re,os,time
from testcsv import testt
def test():
    marks=0
    # fail=testt()
    fail=1
    if fail!=-1:
        with open("ques.csv") as f1 , open("ans.csv") as f2 :
            obj1=csv.reader(f1)
            obj2=csv.reader(f2)
            print("****** EXAM GOING BEGIN ********")
            
            for i in obj1:
                i=str(i).replace("'","")
                ques=str(i)
                ques=ques.replace("[","")
                ques=ques.replace("]","")
                
                for j in obj2:
                    ans=printopt(j,ques)
                    if ans==1:
                        marks+=1
                    break              
                    
        return marks 
    else:
        return -1


            
def printopt(j,que):
    os.system('clear')
    answer=[]
    opt=['A','B','C','D','AB','AC','AD','BC','BD','CD']
    print("\n")
    print(que)
    print("\n")
    result=""
    for k in range(len(j)):
        ret= re.match('\[+[A-D]+\]',j[k])
        if '[' in j[k]:            
            j[k]=j[k].replace("[","")
            j[k]=j[k].replace("]","")      
        if ret != None:
            result=ret.group()
            result=result.replace("[","")
            result=result.replace("]","")
            answer.append(result)
    ##printing options
    for l in range(len(j)):
        print(j[l],end="    ")
        if(l%2!=0):
            print("\n")
    user=input("Enter Your Answer   :")
    if user.upper() not in opt:
        print("In valid  option Enter again")
        time.sleep(2)
        printopt(j,que)
    else:
        act=""
        for i in answer:
            act+=i
        if user.upper() == act:
            return 1
        else:
            return 0
marks=test()
print(f"your marks :{marks}")