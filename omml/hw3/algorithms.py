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
from copy import deepcopy


def gd(filename, x_init, A, y, gamma, 
         l2=0, sparse=True, l1=0, S=1000, max_t=np.inf,
         save_info_period=10, x_star=None, f_star=None):
    m, n = A.shape
    assert(len(x_init) == n)
    assert(len(y) == m)
    if x_star is None:
        x_star = np.zeros(n)
    if f_star is None:
        f_star = 0
    ref_point = np.array(x_star) #если знаем решение, то ref_point поможет вычислять расстояние до него
    x = np.array(x_init)
    
    #эти массивы мы будем сохранять в файл
    its = np.array([0])
    tim = np.array([0.0])
    data_passes = np.array([0.0])
    func_val = np.array([F(x, [A, y, l2, sparse, l1])-f_star])
    sq_distances = np.array([norm(x - ref_point) ** 2])
    
    t_start = time.time()
    num_of_data_passes = 0.0
   
    #метод
    for it in range(S):
        
        #ваш код здесь (возможно, ещё где-то придётся вставить код)
        x -= gamma * logreg_grad_plus_lasso(x, args=[A, y, l2, sparse, l1])
        
        if ((it + 1) % save_info_period == 0):
            its = np.append(its, it + 1)
            tim = np.append(tim, time.time() - t_start)
            data_passes = np.append(data_passes, num_of_data_passes)
            func_val = np.append(func_val, F(x, [A, y, l2, sparse, l1])-f_star)
            sq_distances = np.append(sq_distances, norm(x - ref_point) ** 2)
        if tim[-1] > max_t:
            break
    
    if ((it + 1) % save_info_period != 0):
        its = np.append(its, it + 1)
        tim = np.append(tim, time.time() - t_start)
        data_passes = np.append(data_passes, num_of_data_passes)
        func_val = np.append(func_val, F(x, [A, y, l2, sparse, l1])-f_star)
        sq_distances = np.append(sq_distances, norm(x - ref_point) ** 2)
    #сохранение результатов в файл
    res = {'last_iter':x, 'func_vals':func_val, 'iters':its, 'time':tim, 'data_passes':data_passes,
           'squared_distances':sq_distances}
    
    with open("dump/"+filename+"_GD_gamma_"+str(gamma)+"_l2_"+str(l2)+"_l1_"+str(l1)+"_num_of_epochs_"+str(S)+".txt", 'wb') as file:
        pickle.dump(res, file)
    return res

def FISTA(filename, x_init, A, y, L, 
         mu, sparse=True, l1=0, S=1000, max_t=np.inf,
         save_info_period=10, x_star=None, f_star=None):
    m, n = A.shape
    assert(len(x_init) == n)
    assert(len(y) == m)
    if x_star is None:
        x_star = np.zeros(n)
    if f_star is None:
        f_star = 0
    ref_point = np.array(x_star) #если знаем решение, то ref_point поможет вычислять расстояние до него
    
    #эти массивы мы будем сохранять в файл
    its = np.array([0])
    tim = np.array([0.0])
    data_passes = np.array([0.0])
    xk = np.array(x_init)
    func_val = np.array([F(xk, [A, y, mu, sparse, l1])-f_star])
    sq_distances = np.array([norm(xk - ref_point) ** 2])
    
    t_start = time.time()
    num_of_data_passes = 0.0
    
    yk = np.array(x_init)
    kappa = L / mu
   
    #метод
    for it in range(S):
        
        #ваш код здесь (возможно, ещё где-то придётся вставить код)
        grad_y = logreg_grad(yk, args=[A, y, mu, sparse])
        xk1 = prox_R(yk - grad_y / L, l1 / L)
        yk = xk1 + (np.sqrt(kappa) - 1) / (np.sqrt(kappa) + 1) * (xk1 - xk)
        
        if ((it + 1) % save_info_period == 0):
            its = np.append(its, it + 1)
            tim = np.append(tim, time.time() - t_start)
            data_passes = np.append(data_passes, num_of_data_passes)
            func_val = np.append(func_val, F(xk1, [A, y, mu, sparse, l1])-f_star)
            sq_distances = np.append(sq_distances, norm(xk1 - ref_point) ** 2)
        if tim[-1] > max_t:
            break
            
        xk = xk1
    
    if ((it + 1) % save_info_period != 0):
        its = np.append(its, it + 1)
        tim = np.append(tim, time.time() - t_start)
        data_passes = np.append(data_passes, num_of_data_passes)
        func_val = np.append(func_val, F(xk1, [A, y, mu, sparse, l1])-f_star)
        sq_distances = np.append(sq_distances, norm(xk1 - ref_point) ** 2)
    
    #сохранение результатов в файл
    res = {'last_iter':xk, 'func_vals':func_val, 'iters':its, 'time':tim, 'data_passes':data_passes,
           'squared_distances':sq_distances}
    
    with open("dump/"+filename+"_FISTA_l2_"+str(mu)+"_l1_"+str(l1)+"_num_of_epochs_"+str(S)+".txt", 'wb') as file:
        pickle.dump(res, file)
    return res


def prox_gd(filename, x_init, A, y, gamma, 
         l2=0, sparse=True, l1=0, S=1000, max_t=np.inf,
         save_info_period=10, x_star=None, f_star=None):
    m, n = A.shape
    assert(len(x_init) == n)
    assert(len(y) == m)
    if x_star is None:
        x_star = np.zeros(n)
    if f_star is None:
        f_star = 0
    ref_point = np.array(x_star) #если знаем решение, то ref_point поможет вычислять расстояние до него
    x = np.array(x_init)
    
    #эти массивы мы будем сохранять в файл
    its = np.array([0])
    tim = np.array([0.0])
    data_passes = np.array([0.0])
    func_val = np.array([F(x, [A, y, l2, sparse, l1])])
    sq_distances = np.array([norm(x - ref_point) ** 2])
    
    t_start = time.time()
    num_of_data_passes = 0.0
   
    #метод
    for it in range(S):
        
        #ваш код здесь
        grad_x = logreg_grad(x, args=[A, y, l2, sparse])
        x = prox_R(x - gamma * grad_x, l1 * gamma)
        
        if ((it + 1) % save_info_period == 0):
            its = np.append(its, it + 1)
            tim = np.append(tim, time.time() - t_start)
            data_passes = np.append(data_passes, num_of_data_passes)
            func_val = np.append(func_val, F(x, [A, y, l2, sparse, l1])-f_star)
            sq_distances = np.append(sq_distances, norm(x - ref_point) ** 2)
        if tim[-1] > max_t:
            break
    
    if ((it + 1) % save_info_period != 0):
        its = np.append(its, it + 1)
        tim = np.append(tim, time.time() - t_start)
        data_passes = np.append(data_passes, num_of_data_passes)
        func_val = np.append(func_val, F(x, [A, y, l2, sparse, l1])-f_star)
        sq_distances = np.append(sq_distances, norm(x - ref_point) ** 2)
    
    #сохранение результатов в файл
    res = {'last_iter':x, 'func_vals':func_val, 'iters':its, 'time':tim, 'data_passes':data_passes,
           'squared_distances':sq_distances}
    
    with open("dump/"+filename+"_prox-GD_gamma_"+str(gamma)+"_l2_"+str(l2)+"_l1_"+str(l1)+"_num_of_epochs_"+str(S)+".txt", 'wb') as file:
        pickle.dump(res, file)
    return res

def sgd_decr_stepsize(filename, x_init, A, y, gamma_schedule, 
         l2=0, sparse_full=True, sparse_stoch=False, l1=0, S=50, max_t=np.inf,
         batch_size=1, indices=None, save_info_period=100, x_star=None, f_star=None):
    m, n = A.shape
    assert(len(x_init) == n)
    assert(len(y) == m)
    if indices is None:
        indices = randint.rvs(low=0, high=m, size=min(int(S*m*1.0/batch_size), int(100000/batch_size))*batch_size)
    indices_size = len(indices)
    if x_star is None:
        x_star = np.zeros(n)
    if f_star is None:
        f_star = 0
    ref_point = np.array(x_star) #если знаем решение, то ref_point поможет вычислять расстояние до него
    x = np.array(x_init)
    
    gamma = gamma_schedule[0]
    decr_period = gamma_schedule[1]
    decr_coeff = gamma_schedule[2]
    number_of_decreases = 0
    
    #эти массивы мы будем сохранять в файл
    its = np.array([0])
    tim = np.array([0.0])
    data_passes = np.array([0.0])
    func_val = np.array([F(x, [A, y, l2, sparse_full, l1])-f_star])
    sq_distances = np.array([norm(x - ref_point) ** 2])
    
    t_start = time.time()
    num_of_data_passes = 0.0
    
    if sparse_stoch:
        A_for_batch = A
    else:
        A_for_batch = A.toarray()
    
    indices_counter = 0
    
    c, d = 1, 0
    
    #метод
    for it in range(int(S*m/batch_size)):
        
        #ваш код здесь
        if d >= decr_period * c:
            gamma *= decr_coeff
            c += 1
        if indices_counter == indices_size:
            indices_counter = 0
            indices = randint.rvs(low=0, high=m, size=indices_size)
        batch_ind = indices[indices_counter:(indices_counter+batch_size)]
        indices_counter += batch_size
            
        d += batch_size / m
        g_k = logreg_grad(x, args=[A_for_batch[batch_ind], y[batch_ind], l2, sparse_stoch])
        x = prox_R(x - gamma * g_k, l1 * gamma)
        
        num_of_data_passes += 2.0*batch_size/m
        
        if ((it + 1) % save_info_period == 0):
            its = np.append(its, it + 1)
            tim = np.append(tim, time.time() - t_start)
            data_passes = np.append(data_passes, num_of_data_passes)
            func_val = np.append(func_val, F(x, [A, y, l2, sparse_full, l1])-f_star)
            sq_distances = np.append(sq_distances, norm(x - ref_point) ** 2)
        if tim[-1] > max_t:
            break
    
    if ((it + 1) % save_info_period != 0):
        its = np.append(its, it + 1)
        tim = np.append(tim, time.time() - t_start)
        data_passes = np.append(data_passes, num_of_data_passes)
        func_val = np.append(func_val, F(x, [A, y, l2, sparse_full, l1])-f_star)
        sq_distances = np.append(sq_distances, norm(x - ref_point) ** 2)
    
    #сохранение результатов в файл
    res = {'last_iter':x, 'func_vals':func_val, 'iters':its, 'time':tim, 'data_passes':data_passes,
           'squared_distances':sq_distances}
    
    with open("dump/"+filename+"_SGD_decr_stepsize_gamma_"+str(gamma_schedule[0])+"_decr_period_"
              +str(decr_period)+"_decr_coeff_"+str(decr_coeff)+"_l2_"+str(l2)+"_l1_"+str(l1)+"_num_of_epochs_"+str(S)
              +"_batch_size_"+str(batch_size)+".txt", 'wb') as file:
        pickle.dump(res, file)
    return res


def sgd_const_stepsize(filename, x_init, A, y, gamma, 
         l2=0, sparse_full=True, sparse_stoch=False, l1=0, S=50, max_t=np.inf,
         batch_size=1, indices=None, save_info_period=100, x_star=None, f_star=None):
    m, n = A.shape
    assert(len(x_init) == n)
    assert(len(y) == m)
    if indices is None:
        indices = randint.rvs(low=0, high=m, size=min(int(S*m*1.0/batch_size), int(100000/batch_size))*batch_size)
    indices_size = len(indices)
    if x_star is None:
        x_star = np.zeros(n)
    if f_star is None:
        f_star = 0
    ref_point = np.array(x_star) #если знаем решение, то ref_point поможет вычислять расстояние до него
    x = np.array(x_init)
    
    #эти массивы мы будем сохранять в файл
    its = np.array([0])
    tim = np.array([0.0])
    data_passes = np.array([0.0])
    func_val = np.array([F(x, [A, y, l2, sparse_full, l1])-f_star])
    sq_distances = np.array([norm(x - ref_point) ** 2])
    
    t_start = time.time()
    num_of_data_passes = 0.0
    
    if sparse_stoch:
        A_for_batch = A
    else:
        A_for_batch = A.toarray()
    
    indices_counter = 0
    
    #метод
    for it in range(int(S*m/batch_size)):
        if indices_counter == indices_size:
            indices_counter = 0
            indices = randint.rvs(low=0, high=m, size=indices_size)
            
        #ваш код здесь
        batch_ind = indices[indices_counter:(indices_counter+batch_size)]
        indices_counter += batch_size
        g_k = logreg_grad(x, args=[A_for_batch[batch_ind], y[batch_ind], l2, sparse_stoch])
        x = prox_R(x - gamma * g_k, l1 * gamma)
        
        num_of_data_passes += 2.0*batch_size/m
        
        if ((it + 1) % save_info_period == 0):
            its = np.append(its, it + 1)
            tim = np.append(tim, time.time() - t_start)
            data_passes = np.append(data_passes, num_of_data_passes)
            func_val = np.append(func_val, F(x, [A, y, l2, sparse_full, l1])-f_star)
            sq_distances = np.append(sq_distances, norm(x - ref_point) ** 2)
        if tim[-1] > max_t:
            break
    
    if ((it + 1) % save_info_period != 0):
        its = np.append(its, it + 1)
        tim = np.append(tim, time.time() - t_start)
        data_passes = np.append(data_passes, num_of_data_passes)
        func_val = np.append(func_val, F(x, [A, y, l2, sparse_full, l1])-f_star)
        sq_distances = np.append(sq_distances, norm(x - ref_point) ** 2)
    
    #сохранение результатов в файл
    res = {'last_iter':x, 'func_vals':func_val, 'iters':its, 'time':tim, 'data_passes':data_passes,
           'squared_distances':sq_distances}
    
    with open("dump/"+filename+"_SGD_const_stepsize_gamma_"+str(gamma)+"_l2_"+str(l2)+"_l1_"+str(l1)+"_num_of_epochs_"+str(S)
              +"_batch_size_"+str(batch_size)+".txt", 'wb') as file:
        pickle.dump(res, file)
    return res


def svrg(filename, x_init, A, y, gamma, 
         l2=0, sparse_full=True, sparse_stoch=False, l1=0, S=50, M=None, max_t=np.inf,
         batch_size=1, indices=None, save_info_period=100, x_star=None, f_star=None):
    m, n = A.shape
    assert(len(x_init) == n)
    assert(len(y) == m)
    if M is None:
        M = int(2 * m / batch_size)
    if indices is None:
        indices = randint.rvs(low=0, high=m, size=min(M*batch_size*S, int(100000/batch_size)*batch_size))
    indices_size = len(indices)
    if x_star is None:
        x_star = np.zeros(n)
    ref_point = np.array(x_star) #если знаем решение, то ref_point поможет вычислять расстояние до него
    if f_star is None:
        f_star = 0
    x = np.array(x_init)
    
    #эти массивы мы будем сохранять в файл
    its = np.array([0])
    tim = np.array([0.0])
    data_passes = np.array([0.0])
    func_val = np.array([F(x, [A, y, l2, sparse_full, l1]) - f_star])
    sq_distances = np.array([norm(x - ref_point) ** 2])
    
    t_start = time.time()
    num_of_data_passes = 0.0
    
    if sparse_stoch:
        A_for_batch = A
    else:
        A_for_batch = A.toarray()
    
    indices_counter = 0 #нужен для того, чтобы проходить массив индексов indices
    w = x
    #метод
    for s in range(S):
        # вставьте ваш код здесь
        grad_w = logreg_grad(w, args=[A_for_batch, y, l2, sparse_full])
        num_of_data_passes += 1
        for it in range(M):
            #если закончились индексы, то нужно ещё насэмплировать
            if indices_counter == indices_size:
                indices_counter = 0
                indices = randint.rvs(low=0, high=m, size=indices_size)
            batch_ind = indices[indices_counter:(indices_counter+batch_size)]
            indices_counter += batch_size
            
            #ваш код здесь
            g_k = logreg_grad(x, args=[A_for_batch[batch_ind], y[batch_ind], l2, sparse_stoch])
            g_k -= logreg_grad(w, args=[A_for_batch[batch_ind], y[batch_ind], l2, sparse_stoch])
            g_k += grad_w
            x = prox_R(x - gamma * g_k, l1 * gamma)
            
            num_of_data_passes += 2.0*batch_size/m
            if ((s * M + it + 1) % save_info_period == 0):
                its = np.append(its, s * M + it + 1)
                tim = np.append(tim, time.time() - t_start)
                data_passes = np.append(data_passes, num_of_data_passes)
                func_val = np.append(func_val, F(x, [A, y, l2, sparse_full, l1])-f_star)
                sq_distances = np.append(sq_distances, norm(x - ref_point) ** 2)
        if tim[-1] > max_t:
            break
        w = deepcopy(x)
    
    if ((s * M + it + 1) % save_info_period != 0):
        its = np.append(its, s * M + it + 1)
        tim = np.append(tim, time.time() - t_start)
        data_passes = np.append(data_passes, num_of_data_passes)
        func_val = np.append(func_val, F(x, [A, y, l2, sparse_full, l1])-f_star)
        sq_distances = np.append(sq_distances, norm(x - ref_point) ** 2)
    
    #сохранение результатов в файл
    res = {'last_iter':x, 'func_vals':func_val, 'iters':its, 'time':tim, 'data_passes':data_passes,
           'squared_distances':sq_distances}
    
    with open("dump/"+filename+"_SVRG_gamma_"+str(gamma)+"_l2_"+str(l2)+"_l1_"+str(l1)+"_num_of_epochs_"+str(S)
              +"_epoch_length_"+str(M)+"_batch_size_"+str(batch_size)+".txt", 'wb') as file:
        pickle.dump(res, file)
    return res

