# HOMEWORK 2.5 - Tutorial 2 - Week 1
import timeit

def timeListComp():
    return timeit.Timer(setup="J = {(i,j) for i in range(99) for j in range(i+1,100,1)}")

def timeUnion():
    setup = '''J = set()
for i in range(99):
    for j in range(i+1,100,1):
        J = J.union({(i,j)})'''
    return timeit.Timer(setup=setup)
    
if __name__ == '__main__':
    t = timeListComp()
    time = t.timeit(100)
    print('listcomp time: {t}'.format(t=time))
    t = timeUnion()
    time = t.timeit(100)
    print('union time: {t}'.format(t=time))
    
