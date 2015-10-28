import numpy as np
from copy import copy
import matplotlib.pyplot as plot

sqr_err = []
plot_data = []

in_path = '/Users/keganrabil/Desktop/SP500.txt'
out_path = '/Users/keganrabil/Desktop/SPoutout.txt'

D = {}
index_list = []
z_list = []

p = 30


def order(n,x,train):
    
    d = [0]*n
    for j,key in enumerate(train):
        x_j = train[key][1]
        for i in range(p):
            d[j] += abs(x_j[i] - x[i])
    v = np.argsort(d)
    nhbrs = [train[j][0] for j in v]
    return nhbrs


with open(in_path,"rU") as f:
    f.readline() # Headers
    for string in f:
        try:
            data = string.replace('\n','').split(',')
            index_list.append(float(data[1]))
        except:
            pass  # There is no reading for the day -- Holiday
N = len(index_list)

for i in np.arange(p,N):
    u = [index_list[i] for i in np.arange(i-p,i)]
    u_mean = np.mean(u)
    x = u-u_mean
    z = (index_list[i] - u_mean, x, u_mean)
    if i == p:
        z_list = [z]
    else:
        z_list.append(z)

for i in np.arange(p,N):
    if i==p:
        D[i] = [z_list[i-p]]
    else:
        value = copy(D[i-1])
        value.append(z_list[i-p])
        #print(len(value))
        D[i] = value


for i in np.arange(2*p,N):
    data = copy(D[i])
    z0 = data.pop()
    train = {j:pair for j, pair in enumerate(data)}
    y0 = z0[0]
    x0 = z0[1]
    x_bar = z0[2]


    n = len(train)
    nhbrs = order(n,x0,train)
    
    alpha = 0.25
    s = sum([alpha * (1-alpha) ** i for i in range(n)])
    wts = [(alpha/s) * (1 - alpha)**i for i in range(n)]

    dev = 0
    for j in range(n):
        dev += wts[j]*nhbrs[j]
    y_hat = dev + x_bar

    y0 += x_bar

    sqr_err.append((y0 - y_hat) ** 2)
    if not i%100:
        print("Error:",np.sqrt(sum(sqr_err)/len(sqr_err)))
    plot_data.append([i,y0,y_hat])



plot_mat = np.asmatrix(plot_data)
print(plot_mat.shape)

plot.plot(plot_mat[:,0],plot_mat[:,1],'r',plot_mat[:,0],plot_mat[:,2],'b')
plot.show()

f = open(out_path,'w')
for data in plot_data:
    string = str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "\n"
    f.write(string)
f.close()


