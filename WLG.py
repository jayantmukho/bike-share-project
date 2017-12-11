import math
import numpy as np


class weighted_regression:
    """
        Info here
    """

    def __init__(self,x,y):
        """
            INPUTS:
                   x: feature values (m x n)
                   y: observed values (m x n)
                   tau: weighting parameter
        """


        self.__calculate(x,y)

    def __calculate(self, x, y):
        """
            Main funtion to find ybar
        """
        # find number of examples m and parameters n
        m,n = x.shape

        intercept = np.ones((m,1))
        X = np.concatenate((intercept,x), axis=1)
        XtX=np.dot(X.transpose(),X)
        
        print(XtX)
        theta = np.dot(np.linalg.inv(XtX), X.transpose())
        theta = np.dot(theta,y)

        return self.__decision(X, theta)
        
    def __decision(self, X, theta):
        self.ybar = np.dot(X,theta)
        
    def error_norm(self,y):
        error = self.ybar - y
        norm = np.linalg.norm(error) 
        print(norm)
        m = error.size
        avg_error = np.sum(norm) / m
        return avg_error
    
