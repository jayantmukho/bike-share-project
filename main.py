import sys
import WLG
import numpy as np
import scipy.sparse as sparse
import csv

# CS 229 Project 
# Jessica Lauzon
# Jayant Mukhopadhaya

# SF Bike Share Project

# find data file:
if len(sys.argv) < 2:
    print('Usage:')
    print('  python3 {} <data_file.csv>'.format(sys.argv[0]))
    sys.exit(0)

data_file = sys.argv[1]
params = 11

# ---------------------------------
# parse data file (.csv) to get x y

y = np.loadtxt(data_file, skiprows=1, dtype=np.float64, usecols=(0,), delimiter=',')
x1= np.loadtxt(data_file, skiprows=1, dtype=np.float64, usecols=(1,2,3,4,5,6,7,9), delimiter=',')
day = np.loadtxt(data_file, skiprows=1, dtype=str, usecols=(8,), delimiter=',')
#start_time = np.loadtxt(data_file, skiprows=1, dtype=np.float64, usecols=(9,), delimiter=',')
mean_temp = np.loadtxt(data_file, skiprows=1, dtype=np.float64, usecols=(10,), delimiter=',')

m = y.size 

xday = np.zeros((m, 1))
temp = np.zeros((m, 1))
#time = np.zeros((m, 5))

for i in range(m):
    
    # day of week:
    if day[i] in ['Sat', 'Sun']:
        xday[i] = 1
        
    # temperature:
    if mean_temp[i] < 60:
        temp[(i, 0)] = 1
    
#    # time of day:
#    stime = start_time[i]
#    if stime < 3:       # night
#        time[(i, 0)] = 1
#    elif stime < 6:     # early morning
#        time[(i, 1)] = 1
#    elif stime < 10:    # rush hour
#        time[(i, 2)] = 1
#    elif stime < 15:    # midday
#        time[(i, 3)] = 1
#    elif stime < 19:    # rush hour again
#        time[(i, 2)] = 1
#    elif stime < 22:    # evening
#        time[(i, 4)] = 1
#    else:               # night again
#        time[(i, 1)] = 1

x1.shape      
#time.shape
temp.shape
xday.shape

#x = np.concatenate((x1,time), axis=1)  
x = np.concatenate((x1,temp), axis=1)     
x = np.concatenate((x,xday), axis=1)  


x, indices = np.unique(x, axis=0, return_index=True)
y = np.take(y, indices)
print(y.shape)

with open('full_params_NN1.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(x)
    

np.savetxt("y_vector_NN1.csv", y, delimiter=',', header="duration")

# ---------------------------------
# ----- run linear regression -----

try:
    l = WLG.weighted_regression(x,y)
    norm = l.error_norm(y)
    print(norm)
except RuntimeError as e:
    print('ERROR: {}'.format(e))
    sys.exit(2)
    
    
    
    
    
    
    

