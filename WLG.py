import math
import numpy as np


class LWR:
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
    
    
    
    
    
    