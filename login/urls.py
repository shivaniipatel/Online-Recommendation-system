
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name='login'

urlpatterns = [
        path('', views.index, name='index'),
        path('register/', views.register, name = 'register'),
        path('book_list/', views.book_list, name='book_list'),
        #path('book_list/', views.content_rec, name='content_rec'),
        ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

