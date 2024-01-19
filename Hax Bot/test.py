class Machine:
    # implementation omitted
    pass

class Calculator(Machine):
    # implementation omitted
    pass

class FourFunctionCalculator(Calculator):
    # implementation omitted
    pass
    
if __name__ == '__main__':
    m = Machine()
    c = Calculator()
    f = FourFunctionCalculator()

    print(type(f) == type(c))
    print(type(m) == type(f))
    print(type(m) == type(c))
    print(isinstance(m, Calculator))
    print(isinstance(f, Machine))
    print(isinstance(c, Machine))
    print(isinstance(f, Calculator))