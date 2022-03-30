import nose
from nose.tools import assert_almost_equal, ok_, eq_
from nose.plugins.attrib import attr
from io import StringIO
import numpy as np
import scipy
import scipy.sparse
import scipy.optimize
import sys
import unittest
import warnings

import methods
import oracles


class TestVersion(unittest.TestCase):
    def test_python3(self):
        ok_(sys.version_info > (3, 0))


class TestQuadratic(unittest.TestCase):
    def test_QuadraticOracle(self):
        # Quadratic function:
        #   f(x) = 1/2 x^T x - [1, 2, 3]^T x
        A = np.eye(3)
        b = np.array([1, 2, 3])
        quadratic = oracles.QuadraticOracle(A, b)

        # Check at point x = [0, 0, 0]
        x = np.zeros(3)
        assert_almost_equal(quadratic.func(x), 0.0)
        ok_(np.allclose(quadratic.grad(x), -b))
        ok_(isinstance(quadratic.grad(x), np.ndarray))

        # Check at point x = [1, 1, 1]
        x = np.ones(3)
        assert_almost_equal(quadratic.func(x), -4.5)
        ok_(np.allclose(quadratic.grad(x), x - b))
        ok_(isinstance(quadratic.grad(x), np.ndarray))

        # Check func_direction and grad_direction oracles at
        # x = [1, 1, 1], d = [-1, -1, -1], alpha = 0.5 and 1.0
        x = np.ones(3)
        d = -np.ones(3)
        assert_almost_equal(quadratic.func_directional(x, d, alpha=0.5),
                            -2.625)
        assert_almost_equal(quadratic.grad_directional(x, d, alpha=0.5),
                            4.5)
        assert_almost_equal(quadratic.func_directional(x, d, alpha=1.0),
                            0.0)
        assert_almost_equal(quadratic.grad_directional(x, d, alpha=1.0),
                            6.0)


def check_log_reg(sparse=False):
    # Simple data:
    A = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    if sparse: A = scipy.sparse.csr_matrix(A)
    b = np.array([1, 1, -1, 1])
    reg_coef = 0.5

    # Logistic regression oracle:
    logreg = oracles.create_log_reg_oracle(A, b, reg_coef)

    # Check at point x = [0, 0]
    x = np.zeros(2)
    assert_almost_equal(logreg.func(x), 0.693147180)
    ok_(np.allclose(logreg.grad(x), [0, -0.25]))
    ok_(isinstance(logreg.grad(x), np.ndarray))

    # Check func_direction and grad_direction oracles at
    # x = [0, 0], d = [1, 1], alpha = 0.5 and 1.0
    x = np.zeros(2)
    d = np.ones(2)
    assert_almost_equal(logreg.func_directional(x, d, alpha=0.5),
                        0.7386407091095)
    assert_almost_equal(logreg.grad_directional(x, d, alpha=0.5),
                        0.4267589549159)
    assert_almost_equal(logreg.func_directional(x, d, alpha=1.0),
                        1.1116496416598)
    assert_almost_equal(logreg.grad_directional(x, d, alpha=1.0),
                        1.0559278283039)


class TestLogReg(unittest.TestCase):
    def test_log_reg_usual(self):
        check_log_reg()
        check_log_reg(sparse=True)


    def get_counters(self, A):
        counters = {'Ax': 0, 'ATx': 0, 'ATsA': 0}

        def matvec_Ax(x):
            counters['Ax'] += 1
            return A.dot(x)

        def matvec_ATx(x):
            counters['ATx'] += 1
            return A.T.dot(x)

        def matmat_ATsA(s):
            counters['ATsA'] += 1
            return A.T.dot(A * s.reshape(-1, 1))

        return (matvec_Ax, matvec_ATx, matmat_ATsA, counters)


    def check_counters(self, counters, groundtruth):
        for (key, value) in groundtruth.items():
            ok_(key in counters)
            ok_(counters[key] <= value)


    def test_log_reg_oracle_calls(self):

        A = np.ones((2, 2))
        b = np.ones(2)
        x = np.ones(2)
        d = np.ones(2)
        reg_coef = 0.5

        # Single func
        (matvec_Ax, matvec_ATx, matmat_ATsA, counters) = self.get_counters(A)
        oracles.LogRegL2Oracle(matvec_Ax, matvec_ATx, matmat_ATsA, b, reg_coef).func(x)
        self.check_counters(counters, {'Ax': 1, 'ATx': 0, 'ATsA': 0})

        # Single grad
        (matvec_Ax, matvec_ATx, matmat_ATsA, counters) = self.get_counters(A)
        oracles.LogRegL2Oracle(matvec_Ax, matvec_ATx, matmat_ATsA, b, reg_coef).grad(x)
        self.check_counters(counters, {'Ax': 1, 'ATx': 1, 'ATsA': 0})

        # Single func_directional
        (matvec_Ax, matvec_ATx, matmat_ATsA, counters) = self.get_counters(A)
        oracles.LogRegL2Oracle(matvec_Ax, matvec_ATx, matmat_ATsA, b, reg_coef).func_directional(x, d, 1)
        self.check_counters(counters, {'Ax': 1, 'ATx': 0, 'ATsA': 0})

        # Single grad_directional
        (matvec_Ax, matvec_ATx, matmat_ATsA, counters) = self.get_counters(A)
        oracles.LogRegL2Oracle(matvec_Ax, matvec_ATx, matmat_ATsA, b, reg_coef).grad_directional(x, d, 1)
        self.check_counters(counters, {'Ax': 1, 'ATx': 1, 'ATsA': 0})

        # In a row: func + grad
        (matvec_Ax, matvec_ATx, matmat_ATsA, counters) = self.get_counters(A)
        oracle = oracles.LogRegL2Oracle(matvec_Ax, matvec_ATx, matmat_ATsA, b, reg_coef)
        oracle.func(x)
        oracle.grad(x)
        self.check_counters(counters, {'Ax': 2, 'ATx': 1, 'ATsA': 0})

        # In a row: func + grad + func_directional + grad_directional
        (matvec_Ax, matvec_ATx, matmat_ATsA, counters) = self.get_counters(A)
        oracle = oracles.LogRegL2Oracle(matvec_Ax, matvec_ATx, matmat_ATsA, b, reg_coef)
        oracle.func(x)
        oracle.grad(x)
        oracle.func_directional(x, d, 1)
        oracle.grad_directional(x, d, 2)
        oracle.func_directional(x, d, 2)
        oracle.func_directional(x, d, 3)
        self.check_counters(counters, {'Ax': 6, 'ATx': 2, 'ATsA': 0})

        # In a row: func + grad + func_directional + grad_directional + (func + grad)
        (matvec_Ax, matvec_ATx, matmat_ATsA, counters) = self.get_counters(A)
        oracle = oracles.LogRegL2Oracle(matvec_Ax, matvec_ATx, matmat_ATsA, b, reg_coef)
        oracle.func(x)
        oracle.grad(x)
        oracle.func_directional(x, d, 1)
        oracle.grad_directional(x, d, 2)
        oracle.func_directional(x, d, 2)
        oracle.func_directional(x, d, 3)
        oracle.func(x + 3 * d)
        oracle.grad(x + 3 * d)
        self.check_counters(counters, {'Ax': 8, 'ATx': 3, 'ATsA': 0})


def get_quadratic():
    # Quadratic function:
    #   f(x) = 1/2 x^T x - [1, 2, 3]^T x
    A = np.eye(3)
    b = np.array([1, 2, 3])
    return oracles.QuadraticOracle(A, b)


class TestLineSearch(unittest.TestCase):
    def test_line_search(self):
        oracle = get_quadratic()
        x = np.array([100, 0, 0])
        d = np.array([-1, 0, 0])

        # Constant line search
        ls_tool = methods.LineSearchTool(method='Constant', c=1.0)
        assert_almost_equal(ls_tool.line_search(oracle, x, d, ), 1.0)
        ls_tool = methods.LineSearchTool(method='Constant', c=10.0)
        assert_almost_equal(ls_tool.line_search(oracle, x, d), 10.0)

        # Armijo rule
        ls_tool = methods.LineSearchTool(method='Armijo', alpha_0=100, c1=0.9)
        assert_almost_equal(ls_tool.line_search(oracle, x, d), 12.5)

        ls_tool = methods.LineSearchTool(method='Armijo', alpha_0=100, c1=0.9)
        assert_almost_equal(ls_tool.line_search(oracle, x, d, previous_alpha=1.0), 1.0)

        ls_tool = methods.LineSearchTool(method='Armijo', alpha_0=100, c1=0.95)
        assert_almost_equal(ls_tool.line_search(oracle, x, d), 6.25)
        ls_tool = methods.LineSearchTool(method='Armijo', alpha_0=10, c1=0.9)
        assert_almost_equal(ls_tool.line_search(oracle, x, d), 10.0)

        # Wolfe rule
        ls_tool = methods.LineSearchTool(method='Wolfe', c1=1e-4, c2=0.9)
        assert_almost_equal(ls_tool.line_search(oracle, x, d), 16.0)
        ls_tool = methods.LineSearchTool(method='Wolfe', c1=1e-4, c2=0.8)
        assert_almost_equal(ls_tool.line_search(oracle, x, d), 32.0)


def check_equal_histories(history1, history2, atol=1e-3):
    if history1 is None or history2 is None:
        eq_(history1, history2)
        return
    ok_('func' in history1 and 'func' in history2)
    ok_(np.allclose(history1['func'], history2['func'], atol=atol))
    ok_('grad_norm' in history1 and 'grad_norm' in history2)
    ok_(np.allclose(history1['grad_norm'], history2['grad_norm'], atol=atol))
    ok_('time' in history1 and 'time' in history2)
    eq_(len(history1['time']), len(history2['time']))
    # eq_('x' in history1, 'x' in history2)
    # if 'x' in history1:
    #     ok_(np.allclose(history1['x'], history2['x'], atol=atol))


def check_prototype(method):
    class ZeroOracle2D(oracles.BaseSmoothOracle):
        def func(self, x): return 0.0

        def grad(self, x): return np.zeros(2)

        def hess(self, x): return np.zeros([2, 2])

    oracle = ZeroOracle2D()
    x0 = np.ones(2)
    HISTORY = {'func': [0.0],
               'grad_norm': [0.0],
               'time': [0],  # dummy timestamp
               'x': [np.ones(2)]}

    def check_result(method, max_iter=10000, x0=np.ones(2), history=None):
        method.run(max_iter)
        result = method.hist
        ok_(np.allclose(result['x_star'], x0))

    check_result(method(oracle, x0))
    check_result(method(oracle, x0, 1e-3), 10)
    check_result(method(oracle, x0, 1e-3, {'method': 'Constant', 'c': 1.0}), 10)
    check_result(method(oracle, x0, 1e-3, {'method': 'Constant', 'c': 1.0}), 10, history=HISTORY)
    check_result(method(oracle, x0, 1e-3, line_search_options={'method': 'Constant', 'c': 1.0}), 
                 10, history=HISTORY)
    check_result(method(oracle, x0))
    check_result(method(oracle, x0, tolerance=1e-8), history=HISTORY)


def check_one_ideal_step(method):
    oracle = get_quadratic()
    x0 = np.ones(3) * 10.0
    method = method(oracle, x0, tolerance=1e-5)
    method.run(max_iter=1)
    ok_(np.allclose(method.hist['x_star'], [1.0, 2.0, 3.0]))
    check_equal_histories(method.hist, {'func': [90.0, -7.0],
                                    'grad_norm': [13.928388277184119, 0.0],
                                    'time': [0, 1]  # dummy timestamps
                                    })


def get_1d(alpha):
    # 1D function:
    #   f(x) = exp(alpha * x) + alpha * x^2
    class Func(oracles.BaseSmoothOracle):
        def __init__(self, alpha):
            self.alpha = alpha

        def func(self, x):
            return np.exp(self.alpha * x) + self.alpha * x ** 2

        def grad(self, x):
            return np.array(self.alpha * np.exp(self.alpha * x) +
                            2 * self.alpha * x)

        def hess(self, x):
            return np.array([self.alpha ** 2 * np.exp(self.alpha * x) +
                             2 * self.alpha])

    return Func(alpha)


class TestGradientDescent(unittest.TestCase):
    def test_gd_basic(self):
        check_prototype(methods.GradientDescent)
        check_one_ideal_step(methods.GradientDescent)

    def test_gd_1d(self):
        oracle = get_1d(0.5)
        x0 = np.array([1.0])
        FUNC = [
            np.array([2.14872127]),
            np.array([0.8988787]),
            np.array([0.89869501]),
            np.array([0.89869434]),
            np.array([0.89869434])]
        GRAD_NORM = [
            1.8243606353500641,
            0.021058536428132546,
            0.0012677045924299746,
            7.5436847232768223e-05,
            4.485842052370792e-06]
        TIME = [0] * 5  # Dummy values.
        X = [
            np.array([1.]),
            np.array([-0.42528175]),
            np.array([-0.40882976]),
            np.array([-0.40783937]),
            np.array([-0.40778044])]
        TRUE_HISTORY = {'func': FUNC,
                        'grad_norm': GRAD_NORM,
                        'time': TIME,
                        'x': X}
        # Armijo rule.
        method = methods.GradientDescent(
            oracle, x0,
            tolerance=1e-10,
            line_search_options={
                'method': 'Armijo',
                'alpha_0': 100,
                'c1': 0.3
            }
        )
        method.run(4)
        ok_(np.allclose(method.hist['x_star'], [-0.4077], atol=1e-3))
        check_equal_histories(method.hist, TRUE_HISTORY)
        # Constant step size.
        gd = methods.GradientDescent(
            oracle, x0, tolerance=1e-10, 
            line_search_options={'method': 'Constant','c': 1.0}
        )
        gd.run(max_iter=5)
        ok_(np.allclose(gd.hist['x_star'], [-0.4084371], atol=1e-2))

if __name__ == '__main__':
    unittest.main()
