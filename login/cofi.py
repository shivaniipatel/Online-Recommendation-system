# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 17:24:38 2019

@author: Hp
"""

from numpy import loadtxt
import pandas as pd
import numpy as np
import scipy.optimize as op
   
def cofiCostFunc(params,Y,R ,num_features, Lambda):
    
    num_movies = Y.shape[0]
    num_users = Y.shape[1]

    # reshape the parameter array into parameter matrices
    X = np.matrix(np.reshape(params[:num_movies * num_features], (num_movies, num_features)))  # (1682, 10)
    Theta = np.matrix(np.reshape(params[num_movies * num_features:], (num_users, num_features)))  # (943, 10)

    J = 0
    diff = np.dot(X,Theta.T)
    diff = np.multiply(diff ,R)
    J =0.5*(np.power((diff - Y),2)).sum() + (Lambda/2)*(np.power(Theta,2)).sum() + \
    (Lambda/2)*(np.power(X,2)).sum()
    
    X_Grad = np.dot((diff - Y),Theta) + Lambda*X   
    Theta_Grad = np.dot((diff-Y).T,X) + Lambda*Theta
    
    grad = np.concatenate((np.ravel(X_Grad), np.ravel(Theta_Grad)))
    return J , grad

def recMain(selected_radio):    
    ratings = np.loadtxt(r'C:\Users\Hp\Desktop\cofi\ratings.csv',delimiter=',')
    ratings = ratings[:1000]
    R_bin = np.loadtxt(r'C:\Users\Hp\Desktop\cofi\R_bin.csv',delimiter=',')
    #num_books = ratings.shape[0]     #1000 books
    #num_users = ratings.shape[1]    #5000 users

    Y = ratings
    R = R_bin
    
    Y = np.append(Y, selected_radio, 1)
    idx = np.where(selected_radio!=0)[0]
    
    R_to_append = np.zeros([1000,1])
    for i in idx:   #updating R of new ratings 
        if selected_radio[i] > 0:
            R_to_append[i] = 1
    R = np.append(R,R_to_append,1)
    
    num_books = Y.shape[0]
    num_users = Y.shape[1]
    num_features = 10
    
    X_init = np.random.random([num_books, num_features])   #initializing to random values
    Theta_init = np.random.random([num_users,num_features])

    params = np.concatenate((np.ravel(X_init), np.ravel(Theta_init)))

    a = op.minimize(fun=cofiCostFunc , x0=params ,args=( Y ,R ,10,1)\
                    ,method='CG',jac=True,options={'maxiter':5 })

    #unraveling optimised value
    X = np.array(np.reshape( a.x[:num_books*num_features],(num_books,num_features) ))
    Theta = np.array(np.reshape( a.x[num_books*num_features:],(num_users,num_features) ))

    #predicting ratings for our ratings
    p = np.dot(X,Theta.T)
    my_pred = p[:,-1].reshape([-1,1]) #+ Ymean

    idx = np.argsort(my_pred,0)[::-1]
    idx = idx[:10]

    books =  pd.read_csv(r'D:\books\books_url.csv')
    books = books['title']
    books_rec = ["" for x in range(10)]
    
    c=0
    for i in idx:
        books_rec[c] = books[int(i)]
        c=c+1
        
    return idx
