import numpy as np

a_explanation = '''
EXERCISES 5.9
Problem 3a:

For an n-vector of ones, j, and an n-vector x show:
    inv(n) * j' * x = x_mean


SOLUTION:

First, we recognize that x,j are both vectors of shape (n,1).  Thus,
by the definition of matrix multiplication their product will be a single
number, ie: a matrix of shape (1,1).

By the definition of matrix multiplication we see j' * x is equal to the sum
of their element-wise product:
    j(1)*x(1) + j(2)*x(2) + ... + j(n)*x(n)
    
However, because each element of j is equal to 1 this can be rewritten as:
    x(1) + x(2) + ... + x(n)


By replacing j' * x with this new form in the original equation we see:
    inv(n) * j' * x = inv(n) * sum(x)
    
Notice that n is an integer.  Thus inv(n) is simply 1.0/n.  Therefore we
can rewrite this as:
    sum(x)/n
which is exactly the definition of the mean of an n-vector x.

QED

For an n-vector of ones, j, and an n-vector x
    inv(n) * j' * x = sum(x)/n = avg(x)

'''

b_explanation = '''






Problem 3:

Suppose that the p-vector of sample means x is to be computed from the data matrix X of shape (n,p).
Show:
    x' = inv(j' * j) * j' * X
For j an n-vector of ones.


SOLUTION:

First, we need to define what a p-vector of sample means of X will be.
x will be defined as a p-vector such that:
    x(i) is the mean of the ith row of X for all i in {1,...,p}

Next we shall consider only the multiplication of j' * X.  By the definition of matrix multiplication
this is equal to:
    j' * X = J, where J(i) is equal to the dot product of j and the ith row of X for all i in {1,...,p}
However, because j is a vector of ones this reduces to:
    j' * X = J, where J(i) is equal to the sum of the ith row of X for all i in {1,...,p}

Next we consider the term inv(j' * j).
Because j is an n-vector, the inner term is equal to the dot product of j with itself:
    j' * j = j(1)*j(1) + j(2)*j(2) + ... + j(n)*j(n)
Because every element of j is equal to 1 and there are n elements in j this is equal to:
    j' * j = 1 + 1 + ... + 1 (n times) = n
Because n is an integer, the inverse of n is equal to 1/n.

Thus the whole equation can be rewritten as:
    inv(j' * j) * j' * X = (1/n) * J, where J(i) is equal to the sum of the ith row of X for all i in {1,...,p}
By distributing 1/n through J we arrive at:
    (1/n) * J = x'
This is equal to x' because x is defined to be a vector of shape (n,1), but (1/n) * J has shape (1,n)

QED

x' = inv(j' * j) * j' * X

'''


def c():
    # For sufficiently large n x_t should approach
    # a vector of 0.5 (mean of np.random.random)
    n = 10000
    p = 20
    j = np.matrix(np.ones((n,1)))
    X = np.matrix(np.random.random((n,p)))

        
    # NOTE: This could be improved by replacing np.linalg.inv(j.T * j)
    # with 1./j.shape[0], but in keeping with the spirit of the exercise
    # it is left in its original implementation
    
    # <ONE LINE CALCULATION>
    x_t = np.linalg.inv(j.T * j) * j.T * X
    # </ONE LINE CALCULATION>

    
    print(x_t.T)


if __name__ == '__main__':
    print(a_explanation)
    print(b_explanation)
    c()
    
