from django.shortcuts import render 
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from . import BRS
from . import main
from . import cofi

import csv
import pandas as pd
import numpy as np

from .models import SignIn, Register

import os
filedir = os.path.abspath(os.getcwd())

# Create your views here.

def index(request):  
    
    if request.method=="POST":
    
        if request.POST.get('username') and request.POST.get('password'):   
            entered_username = request.POST.get('username')
            entered_password = request.POST.get('password')
            
            try:
                verify_username = SignIn.objects.get(username=entered_username)
                verify_password = SignIn.objects.get(password=entered_password)
                
                if (verify_username==verify_password):
                    return HttpResponseRedirect(reverse('login:book_list'))
            
            except:
                render(request, 'login/signin.html',{'error_message':'Enter valid details'})
            
            return render(request, 'login/signin.html',{'error_message':'Enter valid details'})
        
        else:
            return render(request, 'login/signin.html',{'error_message':'Enter details'})
    
    else:    
        return render(request, 'login/signin.html')

def register(request):
    
    if request.method=="POST":
        
        if request.POST.get('username') and request.POST.get('password'):
            entered_full_name = request.POST.get('full_name')
            entered_contact = request.POST.get('contact')
            entered_email = request.POST.get('email')
            entered_username = request.POST.get('username')
            entered_password = request.POST.get('password') 
            sn = SignIn(username=entered_username, password=entered_password)
            sn.save()
            reg = Register(signin_details = sn, full_name = entered_full_name, 
                           contact = entered_contact, email = entered_email)
            reg.save()
            return HttpResponseRedirect(reverse('login:book_list'))
        
        else:
            return render(request, 'login/register.html',{'error_message':'Enter details'})   
    
    else: 
        return render(request, 'login/register.html')
    

def book_list(request):
    
    books_url = pd.read_csv('https://res.cloudinary.com/shivaniipatel/raw/upload/v1610867456/Recommendation-dataset/books_url_idm11y.csv',delimiter=',')
    ratings = pd.read_csv('https://res.cloudinary.com/shivaniipatel/raw/upload/v1610867457/Recommendation-dataset/ratings_3_uyvrii.csv',delimiter=',')
    
    book = 'book'
    selected_radio = np.zeros((1000,1))
    selected_radio_to_append = np.zeros((1,3))
    flag = 'FALSE'
        
    #id = data['id']
    title = books_url['bookTitle']
    image_url = books_url['image_url']
    authors = books_url['bookAuthor']
    
    list = [{'title': t[0], 'image_url': t[1], 'authors':t[2], 'selected_radio':t[3] } \
             for t in zip(title, image_url, authors, selected_radio)]
    context ={'list':list}        
    
    if request.method=="POST" and "content_rec" in request.POST:
        for i in range(1000):
            radio_name = book+str(i)
            if request.POST.get(radio_name):
                selected_radio[i,0] = request.POST.get(radio_name)
        
        selected_ISBN = int(request.POST.get('content_rec')) 
        selected_book = books_url.loc[selected_ISBN]
        selected_book = selected_book['bookTitle']  
        
        KNN_rec_books = main.KNN(selected_book)
        KNN_rec_books = pd.DataFrame(KNN_rec_books)
        KNN_rec_books = KNN_rec_books.merge(books_url, how='left', on='ISBN')
        
        KNN_rec_books = [{'bookTitle': t[0], 'bookAuthor': t[1], 'image_url': t[2] } \
             for t in zip(KNN_rec_books['bookTitle'], KNN_rec_books['bookAuthor'], \
                          KNN_rec_books['image_url'])]
        
        flag = 'TRUE'
        
        context ={'list':list, 'flag':flag, 'KNN_rec_books':KNN_rec_books, 'selected_book':selected_book}
        
        return render(request, 'login/book_details.html', context)
        
    
    #radio_name starts from 0 and isbn starts from 1 and also userID
    if request.method=="POST" and "recomm" in request.POST:
        
        for i in range(1000):
            radio_name = book+str(i)
            if request.POST.get(radio_name):
                selected_radio[i,0] = request.POST.get(radio_name)
                
        idx = np.where(selected_radio!=0)
        
        if len(idx[0])==0:
            books_high_mean, books_high_ratings = main.main()
            books_high_mean = pd.DataFrame(books_high_mean)
            books_high_mean = books_high_mean.merge(books_url, how='left', on='ISBN')
        
            books_high_mean = [{'bookTitle': t[0], 'bookAuthor': t[1], 'image_url': t[2] } \
                      for t in zip(books_high_mean['bookTitle'], books_high_mean['bookAuthor'], \
                          books_high_mean['image_url'])]
             
            books_high_ratings = pd.DataFrame(books_high_ratings)
            books_high_ratings = books_high_ratings.merge(books_url, how='left', on='ISBN')
        
            books_high_ratings = [{'bookTitle': t[0], 'bookAuthor': t[1], 'image_url': t[2] } \
                      for t in zip(books_high_ratings['bookTitle'], books_high_ratings['bookAuthor'], \
                          books_high_ratings['image_url'])]
            
            
            flag_zero_ratings = 'TRUE'
            context ={'list':list, 'selected_radio':selected_radio, 'flag_zero_ratings':flag_zero_ratings,\
                      'books_high_mean':books_high_mean, 'books_high_ratings':books_high_ratings}
        
            return render(request, 'login/book_details.html', context)
           
        else:
            print("hello")
        
        #write code to check if selected_radio has all zero values in that case call main.main()
        
        #same format as of ratings(3).csv
        for i in range(1000):
            if selected_radio[i,0]!=0:
                selected_radio_to_append[0,0] = i + 1 #radio_name starts from 0 and isbn starts from 1 
                selected_radio_to_append[0,1] = 5000
                selected_radio_to_append[0,2] = selected_radio[i,0]
                abvgs=1
                for j in range(8500,len(ratings)):
                    if ratings['ISBN'][j] == i+1 :
                        abvgs=0
                if abvgs == 1:
                    with open(rf'{filedir}\dataset\ratings(3).csv','a') as f:
                        writer = csv.writer(f)
                        writer.writerow(selected_radio_to_append[0])
                         
                
        SVD_rec_books = main.SVD() #for calling svd
        #cofi.recMain(selected_radio)
        SVD_rec_books = pd.DataFrame(SVD_rec_books)
        SVD_rec_books = SVD_rec_books.merge(books_url, how='left', on='ISBN')
         
        SVD_rec_books = [{'bookTitle': t[0], 'bookAuthor': t[1], 'image_url': t[2] } \
             for t in zip(SVD_rec_books['bookTitle'], SVD_rec_books['bookAuthor'], \
                          SVD_rec_books['image_url'])]
        
        #flag = 'TRUE'
        
        context ={'list':list, 'selected_radio':selected_radio, 'SVD_rec_books':SVD_rec_books}
        
        return render(request, 'login/book_details.html', context)
        #a return command to return the recommendations    
        
    return render(request, 'login/book_details.html',context)

# 1000 books and 5000 users 
    


#to-do list 
#save selected_radio
#make selected radio array whenever a new customer is registed and not in book_list
#restrict whitesapce in username    
    
#{% for i in "x"|ljust:"1" %}