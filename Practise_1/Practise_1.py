from functools import reduce, lru_cache, wraps, partial , total_ordering
from pymonad   import curry
from math import sqrt
def square(x):
    return x**2

def powerG(x):
 return x+1

s = square(10)
print (s)
# anonymous function 
hello2 = lambda name: print("Hello", name)

# This can not compile :( you need to pass the parhametars hello2()                                                                                  hello2()
hello2("Ziga")
hello2.__qualname__
hello3 = hello2
hello3.__qualname__
hello2.__qualname__= "zigahello"
hello3.__qualname__
hello2.__qualname__
lambda x: x*x
s = lambda x : x + 1
s(60)
# high order function (the tricky is that argument need to pass through objects) 
def choose(grade):
    if grade >5:
        return lambda day: "On " + day + " we celebrate."
    else:
        return lambda points, date:"I scored only " + str(points) +" points. On " + date +   " I’ll have another chance."
print(choose(7))
res = choose(7)
print(res ( "tralala"))
# print (choose( 4, 4))
# high order built-in function)
s1 =map(lambda s : s*3, range (5) )
s2=filter(lambda s: s%2==0 , range(1, 5))
reduce(lambda t, k: t*k , range( 1, 6, 2))

# map and filter with reduce 
add5 = lambda n: n *2
reduce (lambda l , x: l+[add5(x)] , range(10) , [] )
isOdd= lambda n : n%2
reduce(lambda l , x: l +[x] if isOdd else l ,range(10),  [])

# boolean reductions 
# is_lt100 = partial(operator.ge, 100)
# is_gt10 = partial(operator.le, 10)
# from nums import is_prime
# less than 100? # greater than 10?
# implemented elsewhere
# all_pred(71, is_lt100, is_gt10, is_prime)

# function closure 
def addToNx(N):
    def addToN1(i):
        return i+N
    return addToN1
N=10
addToN = addToNx(N)
addToN(7)

# partial aplication
isMap= lambda s: s*5
def addN (i,  f, N) : return i+f(N)
addN10 = partial(addN ,isMap,  N=10, )
addN20 = partial(addN, N=20)
addN10(7)
addN20(7)

# map and filter in Comprehension style
map1 = [x**2 for x in range (1 ,5)]  # None if cond 

filter1 = [x  for x in range(1 ,5) if 5%x ==0 ] 

filterFun =[x for x in range(1, 5) if isOdd(x)]

# Task1: Is it possible to make fold with comprehension? 
# fold1 = [ x+ acc for x in range(1 ,5) if acc>0]

def isPrime(n ): return not [x for x in range(2, int(1 + sqrt(n) ))  if n%x ==0]

findPrime = [ x for x in range( 2, 100) if isPrime(x) ]

# decorators 

#def decor(f):
# def wrapper():
#   print("Inside wraper") 
#   f()
#   return wrapper


#@decor
#def f():
#    print("Inside function")
#    f()

#def decor(f):
#    @wraps(f)
#    def wrapper():
#        print("Called ")
#        f()
#    return wrapper

def test(*args, **kwargs):
    return (args,kwargs)

test(1,2,3,xxx=4)


def decor(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print ("Call ")
        f (*args , **kwargs)
        return wrapper

        
@decor
def f(n):
    if n>0:
       print("g je ")
       f(n-1)

# f= decor(f)
# f()
# f(10)


def memoize(f):
    from collections import OrderedDict
    memoizer = OrderedDict() #{} # Dictionary of pairs args:value
    @wraps(f)
    def wrapper(*args):
        print("usao u wrapper")
        if args not in memoizer:
            print("usao da doda arg" )
            memoizer[args] = f(*args)
            print(memoizer)
        return memoizer[args]
    return wrapper

@memoize
def fib(n):
    s = str(n)
    print("Usao u funkciju sa " + s )
    if n < 2:
        print("Usao u 2 uslov")
        return n
    return fib(n-1) + fib(n-2)

# Memoization (using lru_cache decorator), parameterized decorators
@lru_cache(maxsize =1000)
def fibCache (n):
    if n<2: 
        return n 
    return fibCache(n-1)+ fibCache(n-2)



# fib(35)

fibCache(34)


# currying 

def f(x):
    def f1(y):
        def f2(z):
            return x+y+z
        return f2
    return f1

# s(4 , 3)
# Traceback (most recent call last):
#  File "<stdin>", line 1, in <module>
# TypeError: f1() takes 1 positional argument but 2 were given

# if you pass additional par args you need to handle that par in return case

def m(x, *args):
    def m1(y, *args):
        def m2(z):
            return x+y+z
        if args :
            return m2(*args)
        else: return m2
    if args:
        return m1(*args)
    else: return m1
  

z = m(1 , 2, 3)
print(m(1,2)(3))
print(m(1,2,3))
print(m(1)(2,3))

s = f(5)
t = s(4)
r=t(3)

# curry with decorator 

# fuck you :( take care about spaceeeeeee (one more can make a shit) !!!!!!
def mycurry(f1):

    @wraps(f1)
    def wrappercurry(*args, **kwargs):
        if len(args) + len(kwargs) >= f1.__code__.co_argcount:
            return f1(*args, **kwargs)
        else:
            @wraps(f1)
            def newwrap(*args2, **kwargs2):
                return wrappercurry(*(args + args2), **dict(kwargs, **kwargs2))

            return newwrap

    return wrappercurry


def myCurry(func):
    
    @wraps(func)
    def curried(*args, **kwargs):
        if len(args) + len(kwargs) >= func.__code__.co_argcount:
            # We all the necessary arguments: evaluate func
            return func(*args, **kwargs)
        else:
            # Some arguments still missing: proceed with currying
            @wraps(func)
            def new_curried(*args2, **kwargs2):
                # Merge arguments from current and previous (partial) calls
                print (list(args))
                print(list(args2))
                s= kwargs2.keys
                s1=kwargs2.values
                print (s1)
                print(s)
                return curried(*(args + args2), **dict(kwargs, **kwargs2))

            return new_curried

    return curried

@myCurry
def fcurry(a,b,c):
    return a+b+c

@mycurry
def gcurry(a,b,c):
     return a+b+c

 # iterators

class GocaIter: 
     def __init__(self,  min, max):
         # very pretty way (you don't need to init this variable ) 
         self.current= min
         self.high = max
     def __iter__(self):
        return self
     def __next__(self):
         if self.current>self.high:
             raise StopIteration    
         else: 
             # set the next value 
             self.current+=1
             # return current tj. previous value
             return self.current-1

t = GocaIter(0, 6)
for m in t:
    print(m)

print(list(GocaIter(-2, 0))) # this works 
print(list(t))              # this return [] WHY?????? The point is immediatly after call and later you can not use...


# generators

def GocaGen ( max):
    i=0 
    while i<max:
     yield i
     i+=1

print (list(GocaGen(5)))
print(GocaGen(5))
t= GocaGen(3)
print(list(t)) # immidietly yes and later no !!!

# censoring decorator what ever 

def censor(censor_pred): # Implicitly stores censor_pred in closure
    def censor_p(f):     # Actual decorator with censor_pred in closure
        @wraps(f)
        def wrapper(*args,**kwargs):
           return (x for x in f(*args,**kwargs) if censor_pred(x) ), \
                  (x for x in f(*args,**kwargs) if not censor_pred(x) )
        return wrapper
    return censor_p

def pred(x): 
    return x % 2 == 0

@censor(pred)
def test(n):
    return range(n)

censored, uncensored = test(11)
list(censored), list(uncensored)

# the same scenario it disappear 
#list(censored)
#[]
#list(test(11))
#[<generator object censor.<locals>.censor_p.<locals>.wrapper.<locals>.<genexpr> at 0x040EB4F0>, 
# <generator object censor.<locals>.censor_p.<locals>.wrapper.<locals>.<genexpr> at 0x01412A70>]

#mutual recursion 

def Sierpinski(level, fA, fB, fC, fD):
    fA(level)
    #fB(level)
    #fC(level)
    #fD(level)

def A(level):
    print("A"+str(level),end='')
    if (level > 0): 
        A(level - 1)
        B(level - 1)
        D(level - 1)
        A(level - 1)

def B(level):
    print("B"+str(level),end='')
    if (level > 0): 
        B(level - 1)
        C(level - 1)
        A(level - 1)
        B(level - 1)

def C(level):
    print("C"+str(level),end='')
    if (level > 0): 
        C(level - 1)
        D(level - 1)
        B(level - 1)
        C(level - 1)

def D(level):
    print("D"+str(level),end='')
    if (level > 0): 
        D(level - 1)
        A(level - 1)
        C(level - 1)
        D(level - 1)


Sierpinski(3, A, B, C, D)

#eliminate loop 
do_it=lambda f,*args: f(*args)
map(do_it , [f1,f2,f3])

hello = lambda first, last: print("Hello", first, last)
bye = lambda first, last: print("Bye", first, last)
#sequential program flow 
s=list(map(do_it, [hello, bye],['Goca' , 'jane'], ['vujovic', 'janez']))

# $load C:\Users\Gordana\source\repos\Practise_1\Practise_1\Practise_1.py