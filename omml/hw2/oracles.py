import numpy as np
import scipy
import scipy.sparse

class BaseSmoothOracle(object):
    """
    Base class for implementation of oracles.
    """
    def func(self, x):
        """
        Computes the value of function at point x.
        """
        raise NotImplementedError('Func oracle is not implemented.')

    def grad(self, x):
        """
        Computes the gradient at point x.
        """
        raise NotImplementedError('Grad oracle is not implemented.')
    
    def func_directional(self, x, d, alpha):
        """
        Computes phi(alpha) = f(x + alpha*d).
        """
        return np.squeeze(self.func(x + alpha * d))

    def grad_directional(self, x, d, alpha):
        """
        Computes phi'(alpha) = (f(x + alpha*d))'_{alpha}
        """
        return np.squeeze(self.grad(x + alpha * d).dot(d))


class QuadraticOracle(BaseSmoothOracle):
    """
    Oracle for quadratic function:
       func(x) = 1/2 x^TAx - b^Tx.
    """
    
    def __init__(self, A, b):
        if not scipy.sparse.isspmatrix_dia(A) and not np.allclose(A, A.T):
            raise ValueError('A should be a symmetric matrix.')
        self.A = A
        self.b = b

    def func(self, x):
        # your code here
        return 1 / 2 * x.T @ self.A @ x - self.b.T @ x

    def grad(self, x):
        # your code here
        return self.A @ x - self.b

        
class LogRegL2Oracle(BaseSmoothOracle):
    """
    Oracle for logistic regression with l2 regularization:
         func(x) = 1/m sum_i log(1 + exp(-b_i * a_i^T x)) + regcoef / 2 ||x||_2^2.
    Let A and b be parameters of the logistic regression (feature matrix
    and labels vector respectively).
    For user-friendly interface use create_log_reg_oracle()
    Parameters
    ----------
        matvec_Ax : function
            Computes matrix-vector product Ax, where x is a vector of size n.
        matvec_ATx : function of x
            Computes matrix-vector product A^Tx, where x is a vector of size m.
        matmat_ATsA : function
            Computes matrix-matrix-matrix product A^T * Diag(s) * A,
    """
    def __init__(self, matvec_Ax, matvec_ATx, matmat_ATsA, b, regcoef):
        self.matvec_Ax = matvec_Ax
        self.matvec_ATx = matvec_ATx
        self.matmat_ATsA = matmat_ATsA
        self.b = b
        self.regcoef = regcoef

    def func(self, x):
        # your code here
        bAx = self.b * self.matvec_Ax(x)
        
        # Для решения проблемы overflow encountered
        res = np.zeros_like(bAx)
        res[bAx>=0] = np.log(1 + np.exp(-bAx[bAx>=0]))
        res[bAx<0] = np.log(1 + np.exp(bAx[bAx<0])) - bAx[bAx<0]

        res = np.mean(res)
        res += self.regcoef / 2 * np.linalg.norm(x) ** 2
        return res

    def grad(self, x):
        # your code here
        bAx = self.b * self.matvec_Ax(x)

        # Для решения проблемы overflow encountered
        res = np.zeros_like(bAx)
        res[bAx>0] = - np.exp(-bAx[bAx>0]) / (1 + np.exp(-bAx[bAx>0]))
        res[bAx<=0] = - 1 / (1 + np.exp(bAx[bAx<=0]))
        
        res = self.matvec_ATx(res * self.b) / len(self.b) + self.regcoef * x
        return res


def create_log_reg_oracle(A, b, regcoef):
    """
    Auxiliary function for creating logistic regression oracles.
        `oracle_type` must be either 'usual' or 'optimized'
    """
    # your code here
    matvec_Ax = lambda x: A @ x if isinstance(A, np.ndarray) else A.tocsr() @ x
    matvec_ATx = lambda x: A.T @ x if isinstance(A, np.ndarray) else A.tocsr().T @ x

    def matmat_ATsA(s, A=A):
        # your code here
        if isinstance(A, scipy.sparse.csr_matrix):
            A = A.tocsr()
        return A.T @ s @ A
        
    return LogRegL2Oracle(matvec_Ax, matvec_ATx, matmat_ATsA, b, regcoef)
