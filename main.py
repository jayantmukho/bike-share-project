import sys
import WLG
import numpy as np
import scipy.sparse as sparse

# CS 229 Project 
# Jessica Lauzon
# Jayant Mukhopadhaya

# SF Bike Share Project

# find data file:
if len(sys.argv) < 2:
    print('Usage:')
    print('  python3 {} <data_file.csv> <params>'.format(sys.argv[0]))
    sys.exit(0)

data_file = sys.argv[1]
params = 12

# ---------------------------------
# parse data file (.csv) to get x y

y = np.loadtxt(data_file, skiprows=1, dtype=np.float64, usecols=(0,), delimiter=',')
x1= np.loadtxt(data_file, skiprows=1, dtype=np.float64, usecols=(2,3,4,5,6,7,8,9,10,11,12), delimiter=',')
day = np.loadtxt(data_file, skiprows=1, dtype=str, usecols=(1,), delimiter=',')
m = y.size
xday = np.zeros((m, 1))

for i in range(m):
    if day[i] in ['Sat', 'Sun']:
        xday[i] = 1
    
x = np.concatenate((x1,xday), axis=1)      

# ---------------------------------
# run weighted linear regression
try:
    tau = 5.0
    ybar = WLG.weighted_regression(x,y,tau)
except RuntimeError as e:
    print('ERROR: {}'.format(e))
    sys.exit(2)
    
    

