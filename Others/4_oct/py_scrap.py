def decorator_fun(func):
    def inner(*args, **kwargs):
        [print(i) for i in args]
        print(kwargs['viek'])
        # do operations with func
    func()    
    return inner

@decorator_fun
def func_to():
	print("Inside actual function")

func_to('viv','ek','kkk',viek='vivek')
