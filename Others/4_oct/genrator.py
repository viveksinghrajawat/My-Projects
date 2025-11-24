def simpleGeneratorFun():
    yield 1           
    yield 2           
    yield 3           
for value in simpleGeneratorFun():
    print(value)