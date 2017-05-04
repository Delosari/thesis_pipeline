'''
Created on Jan 22, 2014

@author: vital
'''

# from bisect import bisect

#--------------------Mapping grades------------------------

# def grade(total):
#     return grades[bisect(breakpoints, total)]
# 
# grades = "FEDCBA"
# 
# breakpoints = [30, 44, 66, 75, 85]
# 
# print grade(90)
# 
# print map(grade, [33, 99, 77, 44, 12, 88])


import bisect
import random

# Use a constant see to ensure that we see
# the same pseudo-random numbers each time
# we run the loop.
random.seed(1)

# Generate 20 random numbers and
# insert them into a list in sorted
# order.
l = []
for i in range(1, 20):
    r = random.randint(1, 100)
    position = bisect.bisect(l, r)
    bisect.insort(l, r)
    print '%2d %2d' % (r, position), l

# The first column shows the new random number. The second column shows the position where the number will be inserted into the list. The remainder of each line is the current
# sorted list.
# 
# This is a simple example, and for the amount of data we are manipulating it might be faster to simply build the list and then sort it once. But for long lists, significant time 
#and memory savings can be achieved using an insertion sort algorithm such as this.
# 
# You probably noticed that the result set above includes a few repeated values (45 and 77). The bisect module provides 2 ways to handle repeats. 
#New values can be inserted to the left of existing values, or to the right. The insort() function is actually an alias for insort_right(), which inserts after the existing value. 
#The corresponding function insort_left() inserts before the existing value.
# 
# If we manipulate the same data using bisect_left() and insort_left(), we end up with the same sorted list but notice that the insert positions are different for the duplicate values.













#--------------------Inserting values in list------------------------
print

list = [10, 20, 30]
print "The list before"
print list

print "we do bisect.insort(list, 25)"
print "and we do bisect.insort(list, 15)"

bisect.insort(list, 25)
bisect.insort(list, 15)

print list

#--------------------Find insertion points------------------------

list = [10, 20, 30]
print "The list again, now intersectons"
print list
print "We do bisect.bisect(list, 25)"
print bisect.bisect(list, 15)
print "and we do bisect.bisect(list, 15)"
print bisect.bisect(list, 50)
print "And the list remains"
print list









