print('''
Problem 7.6 # 1: Find the values of r_i that maximize the probability defined in formula 7.5.

We define the Multinomial Distribution as follows (note that subscripts 0 and k have been dropped for convenience):
    P(x|y=A) = N!/(x_1! * ... * x_n!) * (r_1 ^ x_1) * ... * (r_n ^ x_n)
        Where N = sum(x_1,...,x_n) and n is the number of words in the current document.

Our goal is the maximize P(x|y=A) with respect to r_i such that the probability is maximized for all possible
values of x = [x_1,...,x_n] and the sum of all r_i is 1.

We first consider the case where x is a vector of zeros except for some x_j, i <= j <= n, such that x_j = 1.
The first part of the multinomial distribution function {N!/(x_1! * ... * x_n!)} is trivially equal to 1,
thus the maximal probability is acheived by maximizing (r_1 ^ x_1) * ... * (r_n ^ x_n).

However, this can be reduced to r_j since r_i^x_i will be 1 for all i != j.  Since our only other constraint is that
the sum of all r_i is equal to 1 we can maximize this value by setting r_j equal to 1.  Notice this solution
happens to imply that r = x is an optimal solution for this case.  Notice that our selection of j is arbitrary.

Because j can be any index in x and r should be optimal for all possible values of x we see that r must be proportional
to x, r_i = k * x_i for all i.  By adding the constraing that the sum of all r_i is equal to 1 we arrive at the definition
provided in the text:
    r_i = x_i/N for all i.  ''')
