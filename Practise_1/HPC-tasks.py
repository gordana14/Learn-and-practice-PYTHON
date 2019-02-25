#Exercise 1 
#Write a program in C, C++, Fortran, Java or Python that computes an approximation to π using the above formula 
#for the following values of N: 1, 2, 10, 50, 100, 500. For each value of N,
#print out the approximate value π(N) and the error err(N). 
#he error is the difference between π(N) and the true value of π, ie err(N) = π(N) − π. 
#As N increases the value of the error should decrease.
from functools import reduce
from decimal import Decimal
import time
import math

# Method for round floating-point numbers on  double-precision is: round( number, 2)
#  But if I'm used it in function calculateApproximation I didn't see the whole picture in task 2 and 3  

def calculateApproximation (n):
  lsElements = [ (1/ (1 + (((x- 1/2)/n)**2))) for x in range(1, n+1) if n>0 ]
  return reduce(lambda acc , x : acc+ x, lsElements, 0) * (4/n)

def ex1 ():
   N=[1, 2, 10, 50, 100, 500]
   lsResultsAproximation = [(calculateApproximation(s)) for s in N ]
   print ([("%.2f" %  x, "%.2f" %  (x-math.pi) ) for x in lsResultsAproximation ])



# EX2 
#We now want to find out the minimum value of N that is required to give a value for π(N) 
#that is accurate to some specified value. We will call this value Nmin. 
#By computing π(N) f


def ex2():
    fValueCompare =  10**(-6)
    bStop = True
    iCounter=1
    while bStop:
         fError = calculateApproximation(iCounter) - math.pi
         if  fError < fValueCompare:
               bStop = False
               return "%.2f" % iCounter
         else: 
               iCounter+=1

#Execution time 
start_time = time.time()
ex2()
print("--- %s seconds ---" % (time.time() - start_time))

#Exercise 3 
#This way of computing Nmin is clearly inefficient. For example, if we require err(Nmin) < 10−6.
#and we calculate err(2) = 0.02, it is a waste of time to calculate err(3) as it is 
#already obvious that Nmin is very much larger than 2! Rewrite your program so that is uses a more efficient way to 
#locate the minimum value of N.
#Your new method must produce exactly the same value for Nmin as before but should be faster.
#For example, you might try and reduce the number of times that you have to evaluate err(N). 
#ou should also tell us how much faster your new program is


def ex3():
    iCounter=1
    fValueCompare =  10**(-6)
    bStop = True
    iRow = 0
    lsErrors = []
    while bStop:
         expr =  ((iCounter- 1/2)/iCounter)**2 
         # This part needs to be more optimized.
         # I use the highest element  of full calculation, I analyses results in an I see that the element that is greater then 0.99 I can skip 
         # It's import to know,  this is on-line algorithm because it assumes that elements are not known in advance so we can not use method that based sorted elements. 
         if expr * 10 > 9.9: 
            # One additional idea is to define an interval (fError, fError + epsilon) and if next fError (or main element that figure out that value) is there then skip it 
           fError = calculateApproximation(iCounter) - math.pi
           lsErrors.append(fError)
           iRow+=1
           if  fError < fValueCompare:
               bStop = False
               print("%.2f" % iRow) #Here I print a number of times that I evaluated err(N)
               return "%.2f" % iCounter
         iCounter+=1

start_time = time.time()
ex3()
print("--- %s seconds ---" % (time.time() - start_time))        
             
#$load C:\Users\Gordana\source\repos\Practise_1\Practise_1\HPC-tasks.py