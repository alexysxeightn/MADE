import numpy as np
import random
import time

import pickle
from numpy.linalg import norm
from scipy.sparse import csr_matrix
from scipy.optimize import minimize
from scipy.stats import randint
from scipy.stats import bernoulli
from functions import *

def prox_test(your_function):
    with open("dump/prox_test.txt", 'rb') as file:
        test_points, test_lambdas, true_results = pickle.load(file)
    
    for idx, item in enumerate(test_points):
        if norm(true_results[idx] - your_function(item, test_lambdas[idx])) > 1e-6:
            print("Не пройден тест номер ", idx)
            return item, test_lambdas[idx], true_results[idx]
    print("Все тесты пройдены успешно!")
    return 0

def svrg_test(your_result):
    with open("dump/svrg_test.txt", 'rb') as file:
        true_result = pickle.load(file)
    
    if norm(true_result['last_iter'] - your_result['last_iter']) > 1e-6:
        print("Некорректная последняя точка")
        return 1
    for idx, item in enumerate(your_result['func_vals']):
        if abs(true_result['func_vals'][idx] - item) > 1e-6:
            print("Некорректное сохранённое значение в массиве значений на позиции ", idx)
            return 1
    
    print("Тесты пройдены!")
    return 0

def sgd_const_test(your_result):
    with open("dump/sgd_const_test.txt", 'rb') as file:
        true_result = pickle.load(file)
    
    if norm(true_result['last_iter'] - your_result['last_iter']) > 1e-6:
        print("Некорректная последняя точка")
        return 1
    for idx, item in enumerate(your_result['func_vals']):
        if abs(true_result['func_vals'][idx] - item) > 1e-6:
            print("Некорректное сохранённое значение в массиве значений на позиции ", idx)
            return 1
    
    print("Тесты пройдены!")
    return 0

def sgd_decr_test(your_result):
    with open("dump/sgd_decr_test.txt", 'rb') as file:
        true_result = pickle.load(file)
    
    if norm(true_result['last_iter'] - your_result['last_iter']) > 1e-6:
        print("Некорректная последняя точка")
        return 1
    for idx, item in enumerate(your_result['func_vals']):
        if abs(true_result['func_vals'][idx] - item) > 1e-6:
            print("Некорректное сохранённое значение в массиве значений на позиции ", idx)
            return 1
    
    print("Тесты пройдены!")
    return 0

def prox_gd_test(your_result):
    with open("dump/prox_gd_test.txt", 'rb') as file:
        true_result = pickle.load(file)
    
    if norm(true_result['last_iter'] - your_result['last_iter']) > 1e-6:
        print("Некорректная последняя точка")
        return 1
    for idx, item in enumerate(your_result['func_vals']):
        if abs(true_result['func_vals'][idx] - item) > 1e-6:
            print("Некорректное сохранённое значение в массиве значений на позиции ", idx)
            return 1
    
    print("Тесты пройдены!")
    return 0
    
def fista_test(your_result):
    with open("dump/fista_test.txt", 'rb') as file:
        true_result = pickle.load(file)
    
    if norm(true_result['last_iter'] - your_result['last_iter']) > 1e-3:
        print("Некорректная последняя точка")
        return 1
    for idx, item in enumerate(your_result['func_vals']):
        if abs(true_result['func_vals'][idx] - item) > 1e-3:
            print("Некорректное сохранённое значение в массиве значений на позиции ", idx)
            return 1
    
    print("Тесты пройдены!")
    return 0

def gd_test(your_result):
    with open("dump/gd_test.txt", 'rb') as file:
        true_result = pickle.load(file)
    
    if norm(true_result['last_iter'] - your_result['last_iter']) > 1e-6:
        print("Некорректная последняя точка")
        return 1
    for idx, item in enumerate(your_result['func_vals']):
        if abs(true_result['func_vals'][idx] - item) > 1e-6:
            print("Некорректное сохранённое значение в массиве значений на позиции ", idx)
            return 1
    
    print("Тесты пройдены!")
    return 0