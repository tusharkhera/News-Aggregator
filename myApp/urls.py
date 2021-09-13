from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.pro_page, name='home'),
    path('', views.pro_page, name='home'),
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.log_in, name='log_in'),
    path('pro/', views.pro_page, name='pro_page'),
    path('logout/', views.log_out, name='log_out'),
    path('changepassword/', views.change_pass, name="change_pass"),
    path('forgotpassword/', views.forgot_pass, name='forgot_pass'),
    path('donation/', views.donate_us, name='donate_us'),
    path('handlerequest/', views.handleRequest, name='handle_request'),
    path('indnews/', views.indNews, name='ind_news'),
    path('worldnews/', views.wrdNews, name='wrd_news'),
    path('search/', views.search, name='search')
]
