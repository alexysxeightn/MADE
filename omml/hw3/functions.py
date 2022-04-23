import numpy as np
import random
import time

from numpy.linalg import norm
from scipy.sparse import csr_matrix
from scipy.optimize import minimize
from scipy.special import expit


def least_squares_val(x, args):
    A = args[0]
    b = args[1]
    return (norm(A.dot(x) - b) ** 2) * 1.0 / (2*A.shape[0])

def least_squares_grad(x, args):
    A = args[0]
    b = args[1]
    return (A.T.dot(A.dot(x)) - A.T.dot(b)) * 1.0 / A.shape[0]

def logreg_loss(x, args):
    A = args[0]
    y = args[1]
    l2 = args[2]
    sparse = args[3]
    assert l2 >= 0
    assert len(y) == A.shape[0]
    assert len(x) == A.shape[1]
    degree1 = np.zeros(A.shape[0])
    if sparse == True:
        degree2 = -(A * x) * y
        l = np.logaddexp(degree1, degree2)
    else:
        degree2 = -A.dot(x) * y
        l = np.logaddexp(degree1, degree2)
    m = y.shape[0]
    return np.sum(l) / m + l2/2 * norm(x) ** 2

def logreg_grad(x, args):
    A = args[0]
    y = args[1]
    mu = args[2]
    sparse = args[3]
    assert mu >= 0
    assert len(y) == A.shape[0]
    assert len(x) == A.shape[1]
    if sparse == True:
        degree = -y * (A * x)
        sigmas = expit(degree)
        loss_grad = -A.transpose() * (y * sigmas) / A.shape[0]
    else:
        degree = -y * (A.dot(x))
        sigmas = expit(degree)
        loss_grad = -A.T.dot(y * sigmas) / A.shape[0]
    assert len(loss_grad) == len(x)
    return loss_grad + mu * x

def logreg_grad_plus_lasso(x, args):
    return logreg_grad(x, args) + args[4] * np.sign(x)

def r(x, l1):
    assert (l1 >= 0)
    return l1 * norm(x, ord = 1)

def F(x, args):
    return logreg_loss(x, args) + r(x, args[4])
