import math
import numpy as np


class weighted_regression:
    """
        Info here
    """
    
    def __init__(self,x,y,tau):
        """
            INPUTS:
                   x: feature values (m x n)
                   y: observed values (m x n)
                   tau: weighting parameter
        """
        
        
        self.__calculate(x,y,tau)
    
    def __calculate(self, x, y, tau):
        """
            Main funtion to find ybar
        """
        # find number of examples m and parameters n
        m,n = x.shape
        
        intercept = np.ones((m,1))
        X = np.concatenate((intercept,x), axis=1)
        
        theta = np.random.rand((n,1))*0.1
        for i in range(m):
            for j in range(n):
                h = np.dot()
                theta 
                
        
    def __decision(self, X, theta):
        return ybar = np.dot(X*theta)
    
    
    