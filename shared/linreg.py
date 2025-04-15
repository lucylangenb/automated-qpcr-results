###
### Functions to perform linear regression and subsequent quantification of HIVDR samples.
###
### These functions are stored in a separate file so that algorithms can be edited more easily, if needed.
###

import numpy as np
import pandas as pd


# Helper function - get standard curve using least squares.
#
# From Georgia Tech:
# |
# | Let 'A' be an 'm' x 'n' matrix and let 'b' be a vector in R^m. 
# | A least-squares solution of the matrix equation 'Ax = b' is a vector 'x^' in R^n such that:
# |     dist(b, Ax^) <= dist(b, Ax)
# | for all other vectors 'x' in R^n.
# |
# | In other words, the least-squares solutions of 'Ax = b' are the solutions of the matrix equation:
# |     (A^T)Ax = (A^T)b
# | Thus, the least squares solution can be found by:
# |     1. Compute the matrix (A^T)A and the vector (A^T)b.
# |     2. Form the augmented matrix equation (A^T)Ax = (A^T)b, and row reduce.
# |     3. This equation is always consistent, and any solution x^ is a least-squares solution.
# |
# See more: https://textbooks.math.gatech.edu/ila/least-squares.html
#
# Applied here, least squares is used as follows:
#   y = mx + b
#   which can be rewritten as
#   y = A[m, b]
#   where [m] is the vertical vector x^
#         [b]
#   and A is the coefficient matrix that transforms x^ into y.
#   Applying A^T - "A transform" - to both sides, we get
#   A^T y = A^T A x^
#   where A^T A is equal to the identity matrix. Thus,
#   A^T y = I x^ = x^
#   which allows us to solve for x^.
# Here, x^ is the effective copy number, while y is the Cq/Ct value.
# Given y, we can solve for x^.

def linreg(df, fluor='CY5', percent_drm=0.2):
    '''Let `y = mx + b` be the linear standard curve applied to data,
    where `x` is the log10 quantity (input copies per reaction),
    while `y` is the resulting Cq/Ct. Given standard curve data - 
    in the form of `(x, y)` pairs that can be extracted from a pandas dataframe - 
    this function returns the slope and intercept of the standard curve, 
    calculated using least squares regression.
    
    Args:
        df (pd.DataFrame): data containing standard curve data (copies, Cq)
        fluor (str): fluorophore Cq data used to construct curve
        percent_drm (float): for non-VQ fluorophores, define the constant percentage DRM (for example, if standards are all 20% DRM, linreg will multiply all VQ copies by 0.2 to get DRM copies)
    Returns:
        (m, b) (float tuple): slope and intercept, as used in linear regression `y = mx + b`'''
    
    data = df.loc[df['Assigned Quantity'].notnull(), #only rows with assigned copy numbers - *not* NaN
                     ['Assigned Quantity', f'{fluor} CT']] #only columns with 'x' and 'y' data
    
    if fluor != 'CY5':
        data['Assigned Quantity'] = data['Assigned Quantity'].mul(percent_drm) #controls have 20% DRMs - multiply VQ quant by 0.2 to get DRM quant

    x = np.array(data['Assigned Quantity'].apply(np.log10)) #get log10 of quantity - 'x'
    y = np.array(data[f'{fluor} CT']) #get Cq values - 'y'

    A = np.vstack([x, np.ones(len(x))]).T #create coefficient matrix - coefficients in left column for m, "1" in right column to leave b unaffected
    m, b = np.linalg.lstsq(A,y, rcond=None)[0] #0 specifies that we only want the least squares solution, not residuals

    return m, b


# helper function - get quantity based on standard curve regression
# in regression, y=mx+b ==
# (Cq) = m*(log10 copies) + b
def quantify(y, m, b):
    '''Given `y = mx + b` --> `(Cq) = m*(log10 copies) + b`, solve for `10^x` (copies) using Cq.
    Args:
        y (float): Cq value
        m (float): slope to use
        b (float): intercept to use
    Returns:
        x (float): copies, converted from log10 into true copies
    '''
    x = (y-b)/m
    return 10**x