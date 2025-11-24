memory = {}
def memoize_factorial(f):
    def inner(num):
        if num not in memory:
            memory[num] = f(num)
            print('result saved in memory')
        else:
            print('returning result from saved memory')
        return memory[num]
 
    return inner
     
@memoize_factorial
def facto(num):
    if num == 1:
        return 1
    else:
        return num * facto(num-1)
 
print(facto(5))
print(facto(7)) # directly coming from saved memory

# ***************3********************
# def decodecorator(dataType, message1, message2):
#     def decorator(fun):
#         print(message1)
#         def wrapper(*args, **kwargs):
#             print(message2)
#             if all([type(arg) == dataType for arg in args]):
#                 return fun(*args, **kwargs)
#             return "Invalid Input"
#         return wrapper
#     return decorator
 
 
# @decodecorator(str, "Decorator for 'stringJoin'", "stringJoin started ...")
# def stringJoin(*args):
#     st = ''
#     for i in args:
#         st += i
#     return st
 
 
# @decodecorator(int, "Decorator for 'summation'\n", "summation started ...")
# def summation(*args):
#     summ = 0
#     for arg in args:
#         summ += arg
#     return summ
 
 
# print(stringJoin("I ", 'like ', "python"))
# print()
# print(summation(19, 2, 8, 533, 67, 981, 119))

#*****************2**************************

# def decor1(func):
#     def inner():
#         x = func() # x=20 since decor() return 2*10
#         return x * x
#     return inner
 
# def decor(func):
#     def inner():
#         x = func()  #x=10 since func() returning 10
#         return 2 * x
#     return inner
 
# @decor1
# @decor
# def num():
#     return 10
 
# print(num()) #simlar to decor1(decor(num()))