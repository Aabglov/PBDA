# HOMEWORK 2.3 - Tutorial 2 - Week 1


def a():
    print '''\nlst1 is a list of sets of tuples of all pairs of values from 0 to 4 (non-inclusive).
    Each set contains all tuples of pairs of values i and j.\n\n'''

def b():
    print '''When i == j this set would produce two tuples of form (i,j) and (j,i). 
    However, because these values are equal we can rewrite them as (i,i) and (i,i). 
    These tuples are stored within a set and because a set cannot contain duplicate entries 
    the second is not included.\n\n'''

def c():
    print '''\nThe construction of these two lists are nearly identical, however lst2 includes an
    additional statement at the end (if i != j).  This stipulation prevents an entry from being
    created if i == j.  Thus, {(0,0)},{(1,1)},{(2,2)},{(3,3)} are not generated because i is
    equal to j at these steps.'''
    
if __name__ == '__main__':
    lst1 = [{(i,j),(j,i)} for i in range(5-1) for j in range(i,5-1,1)]
    print lst1
    a()
    b()
    lst2 = [{(i,j),(j,i)} for i in range(5-1) for j in range(i,5-1,1) if i != j]
    print lst2
    c()
