from django.db import models

# Create your models here.

class SignIn(models.Model):
    username = models.CharField(max_length=15, null=True, blank=True, unique=True)
    password = models.CharField(max_length=15, null=True)
    def __str__(self):
        return self.username
    
class Register(models.Model):
    signin_details = models.OneToOneField(SignIn, on_delete=models.CASCADE,null=True, blank=True)
    full_name = models.CharField(max_length=15, null=True)
    contact = models.IntegerField(null=True)
    email = models.EmailField(null=True) 
    def __str__(self):
        return self.full_name
    
class BookDetails(models.Model):
    user_details = models.ManyToManyField(SignIn)
    book_name = models.CharField(max_length=30, null=True)
    price = models.IntegerField(null=True)
    def __str__(self):
        return self.book_name
    #username, book id, ratings 
    
    
#for every user there is an array of books rating
