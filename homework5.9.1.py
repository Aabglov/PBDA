explanation = '''
EXERCISES 5.9
Problem 1:

Suppose s is a statistic and that for any two sets D1 and D2 that form a partition of the set D:
    s(D1 U D2) = s(D1) + s(D2).  For a partition of D with cardinality k show s(D) = s(D1) + s(D2) + ... + s(Dk)


SOLUTION:

By definition of a partition we see that s(D) can be rewritten as s(D1 U D2 U ... U Dk).

We will now show s(D1 U D2 U ... U Dk) =  s(D1) + s(D2) + ... + s(Dk) via Induction.



    Base Case: for a partition of 1 element, show s(D1) = s(D).  This case is trivially true
    because a partition of 1 element is the set itself.



    Iterative Case: Assume the k-case holds. IE:
        s(D1 U D2 U ... U Dk) = s(D1) + s(D2) + ... + s(Dk)
    Show the k+1-case also holds.

    Consider a partition of D: D1,D2,...,Dk,Dk+1.  For convenience we call (D1 U D2 U ... U Dk) = K.
    Notice K U Dk+1 is a 2 element partition of D.

    By the statement of this problem we know s(D1 U D2) = s(D1) + s(D2).  Thus s(K U Dk+1) = s(K) + s(Dk+1).
    However, by the supposition of the iterative case we can rewrite this as:
    s(K U Dk+1) = s(D1) + s(D2) + ... + s(Dk) + s(Dk+1)

    By substituting the defintion of K we see:
        s(D1 U D2 U ... U Dk U Dk+1) = s(D1) + s(D2) + ... + s(Dk) + s(Dk+1)

        

By showing both the base case and iterative case this statement must hold for all integer values of k >= 1.

QED
For any partition of k elements of a set D,
    s(D) = s(D1 U D2 U ... U Dk) = s(D1) + s(D2) + ... + s(Dk)



'''

        

if __name__ == '__main__':
    print(explanation)
