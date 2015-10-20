import functools

a = 5
b = 10

# クロージャ
def foo(a):
    def wrap(b):
        return  a + b

    return wrap

foo_closure = foo(a)
print('closure', foo_closure(b))

def func(a, b):
    return a + b

# functools.partial
foo_partial = functools.partial(func, a=a)
print('partial', foo_partial(b))

# lambda
foo_lambda = lambda b: func(a, b)
print('lambda', foo_lambda(b))

# クラス

class Func(object):
    def __init__(self, a):
        self.a = a

    def __call__(self, b):
        return self.a + b

foo_class = Func(a)
print('class', foo_class(b))
