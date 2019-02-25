# exam 2 2016-2017 
#In Python we want to implement a strict censorship policy.
#For each function that returns a list, this policy will be defined with a censorship predicate (censor_pred). 
#Implement a decorator censor that will, for a given list-returning function,
#check its elements according to the provided predicate, and return a 
#pair (tuple) of generators that contain only the censored/uncensored elements. 
#Hint: remember closures and higher-order functions. Example of usage: 
from math import factorial
from functools import reduce, lru_cache, wraps, partial , total_ordering
import random
def censor(censor_pred): # Implicitly stores censor_pred in closure
    def censor_p(f):     # Actual decorator with censor_pred in closure
        @wraps(f)
        def wrapper(*args,**kwargs):
           
           return  zip(list (x  for x in f(*args,**kwargs) if censor_pred(x) ), 
                   list (x for x in f(*args,**kwargs) if not censor_pred(x) )
                   )
        return wrapper
    return censor_p

def pred(x): 
    return x % 2 == 0

@censor(pred)
def test(n):
    return list(n)

censored, uncensored = test([1,2,3,4])
list(censored), list(uncensored)

#exam 1 2017 -2018
#Generation of  (fractal) numbers from Mandelbrot set is defined inductively as follows: 
#    • Initial value:   𝑍𝑍0=0+0𝑗𝑗    (complex zero)
#   • Inductive step:   𝑍𝑍𝑛𝑛+1=𝑍𝑍𝑛𝑛 2 + 𝑐𝑐  (c is a complex constant, eg. c=0.1+0.2j)  
#   Hint : in Python computations with complex numbers are sintactically equivalent to operations with real numbers (we can also use the same functions).
#  The procedure should generate numbers until it reaches the maximal number of steps (parameter maxstep) or until |𝑍𝑍𝑛𝑛|>2, 
# what can be checked in Python with expression abs(Zn)>2. 
# a) In programming language Python define the generator function Mandelbrot(c, maxstep)that generates the numbers as described. 
# b) Write a short program that prints out all results of the Mandelbrot generator with parameters 
# 𝑐𝑐=0.2+ 0.7𝑗𝑗  and maxstep=100. 
# For each result it shoult print its sequential number,  value (complex number), and absolute value (real number). 
# Hint (Python code):   c = 0.2 + 0.7j  # A complex number in Python print(1, c, abs(c)) # Print-out as above 
# c) Could we use a generator expression instead of generator function in (a)? 
# If yes, write an appropriate generator expression; if no, explain your reasoning. 

def Mandelbrot( c , maxstep):
    i=0
    a= complex(0.0, 0.0)
    while (i<maxstep or abs(a)>2):
        yield a 
        a=abs(a)**2 + c
        i+=1

def stampa (*args ):
    s=Mandelbrot(complex(args[0], args[1]), args[2])
    for i, number in zip(range(args[2]) ,s):
     print(number,  i , abs(number))

stampa(0.0, 0.7, 5)

#mandelbrot2 = (abs(a)+complex(0.0, 0.7) for a in zip(range(5), range(5)))

# Exam 1 2014/2015
#In Python programming language choose a mechanism that uses lazy evaluation and returns elements of the above infinite sum.
#Use this mechanism to implement a sequence of elements representing increasingly improved approximations of 𝑒𝑥: 
#(each (k-th) sequence element is therefore a previous sum with an additional term 𝑥𝑘 𝑘!) 
def sumOfEonPowerX ( x):
    a=1
    i=1
    while True:
        yield a 
        a=a + (x**i)/factorial(i)
        i+=1


from itertools import tee, accumulate
s, t = tee(sumOfEonPowerX(2))
pairs = zip(t, accumulate(s))
for _, (iter, sum) in zip(range(7), pairs):
    print(iter, sum)

s1= sumOfEonPowerX(2)

res=reduce(lambda l,s :l+s[1] , zip(range(7), s1), 0)

#exam2 2017 ~2018
#Consider a higher-order Python function group that is a generalization of the reduce (fold) function.
#It works on lists of pairs (key, value) by grouping together all the elements with the same key and performing aggregation on each group. 
#def group(data, aggregator, initial_value): where data is a list of (key, value) pairs,
#aggregator is a function of two arguments (as for reduce or fold) and
#initial_value is the initial aggregation value with the default value 0. 

lspairs =[(random.randint(1, 10) , random.randint(10, 10000)) for i in range(1, 10) ]

def koliko(s, ls):
    return ls.count(s)

def group (data, agregate, initial_value):
    auxList =[]
    lsKey=list(map (lambda t: t[0] , data))
    lscopy = lsKey.copy()
    lsDuplicate= list(set(lscopy))
 
    #res =map(lambda x: auxList.append(x) if (x not in auxList) else False,  list(lsKey))
    res =list(map(lambda t :list(filter(lambda s: s[0]==t, data)), lsDuplicate ))
    final =  reduce (lambda s2, t2: reduce(lambda s1, t1: agregate(t1[0], s1[1]) +t1 , t2 , 0) +t2 , data , 0)
    return final
    
s= group(lspairs,[], [])
# print(list(s))
#Provide examples of group calls for SUM, COUNT, MIN, and MAX of values, including aggregator definitions with anonymous functions. 
#A generic function call example and results for the above data value: 
# Can you also provide the group call for aggregator AVG (average of values). 
# If yes, give an example group call and if not explain why. 


# exam 3 2016-2017
#Define the higher-order function    
#   map_filter_set(iterable, map_function, filter_predicate)    
# with the following arguments: 
#     • iterable: any iterable object 
#     • map_function: a function that maps an element from iterable 
#     • filter_predicate: a predicate that returns True for acceptable mapped elements 
# The function applies the map_function on each element from iterable and returns a set of values for which the filter_predicate is True. 
 
def map_filter_set (iterable, map_function, filter_predicate):
  return set(reduce ( lambda acc, t: acc+[map_function(t)] if filter_predicate(map_function(t)) else acc , iterable, []))


#Use the function map_filter_set and partial application to define a function squares3 that returns a set of squared elements from iterable, divisible by 3.  

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


MapPom= lambda n: n**2
isOdd=lambda n: n%3==0
result = map_filter_set(GocaIter(0,5), MapPom, isOdd)
# it doesn't work !!! https://docs.python.org/2/library/functools.html
squares3= partial(map_filter_set, GocaIter(0,5), MapPom, isOdd )

##exam 1 2016-2017 
#In lectures we discussed how to implement a currying decorator in Python by hand. 
#For this task we will consider only positional arguments. 
#a) Implement a decorator named curry3, that, for an arbitrary function that
#(in its uncurried form) accepts exactly three (3) positional arguments, 
#prints out how many arguments were curried, and proceeds with the actual function evaluation. For example: 

def curry3(f1):
    # using a global for brevity
    counter=0
    @wraps(f1)
    def wrappercurry(*args):
         if len(args) >= f1.__code__.co_argcount:
            nonlocal  counter
            counter=counter+1
            print ("Curried parameters: "+ str(counter))
            counter = 0
            return f1(*args)
         else:
            @wraps(f1)
            def newwrap(*args2):
                 nonlocal  counter
                 counter = counter + 1
                # print("current "+ str(counter))
                 return wrappercurry(*(args + args2))

            return newwrap
    return wrappercurry



@curry3
def fcurry(a,b,c):
    return a+b+c

fcurry(1)(3)(4)

fcurry(1)(4,3)
fcurry(1,3,4)

# $load C:\Users\Gordana\source\repos\Practise_1\Practise_1\Exams.py
#Obavezno za procitati !!!!!
# http://blog.dhananjaynene.com/2013/10/partially-applied-functions-and-decorators-in-python/
# https://mtomassoli.wordpress.com/2012/03/18/currying-in-python/
# https://www.programcreek.com/python/example/708/functools.wraps
# https://hynek.me/articles/decorators/