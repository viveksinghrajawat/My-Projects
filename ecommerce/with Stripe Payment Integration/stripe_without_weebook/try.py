# arr = [5,7,8,1,3,6,9,3,2]
# for i in range(len(arr)):
#     t=abs(arr[i]-9)
#     if t in arr:
#         temp=arr.index(t)
#         if temp > i :
#             print(arr[i],t)

orderid=['1','A']
x = len(orderid)
for i in range(30):
    # print(len(order_id))
    orderid=list(orderid)
    if orderid[len(orderid)-1] == 'Z':
        orderid[len(orderid)-1] = 'A'
        orderid.append('A')
    orderid[-1]=chr(ord(orderid[-1]) + 1)
    orderid = ''.join(orderid)
    orderid=orderid.ljust(8,'A')
    print(orderid)
    # if order_id[x-1] == 'Z':
    #     order_id[x-1] = 'A'
    #     order_id.append('A')
    #     y=''.join(order_id)
    #     print(y)
    # else:
    #     order_id[x-1]=chr(ord(order_id[x-1]) + 1)
    #     y=''.join(order_id)
    #     print(y)