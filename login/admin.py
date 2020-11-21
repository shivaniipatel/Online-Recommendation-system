from django.contrib import admin
from .models import SignIn, Register, BookDetails 

# Register your models here.

admin.site.register(SignIn)
admin.site.register(Register)
admin.site.register(BookDetails)