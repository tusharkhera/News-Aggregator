
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, HttpResponseRedirect
from requests.sessions import Request
from .forms import SignUpForm , donateForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm , PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
import requests
from bs4 import BeautifulSoup
import json

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

def home(request):
    if request.user.is_authenticated:
        return render(request, 'pro.html', {'name':request.user, 'news':news})
    else:    
        return render(request, 'home.html')     

def sign_up(request):
    if request.method == 'POST':
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Account created successfully !!')
            fm.save()    
            fm = SignUpForm()    
    else:        
        fm = SignUpForm()
    return render(request, 'signUp.html', {'form':fm})

def log_in(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully')
                    return HttpResponseRedirect('/pro/')
        else:            
            fm = AuthenticationForm()
        return render(request, 'login.html', {'form':fm})
    else:
        return HttpResponseRedirect('/pro/')    

def log_out(request):
    logout(request)
    return HttpResponseRedirect('/home/')    

def change_pass(request):
    if request.user.is_authenticated:
        if request.method =='POST':
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Password changed successfully')
                return HttpResponseRedirect('/pro/')
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request, 'changePass.html', {'form':fm})
    else:
        return HttpResponseRedirect('/login/')        

def forgot_pass(request):        
    if request.method =='POST':
        fm = SetPasswordForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            # update_session_auth_hash(request, fm.user)
            messages.success(request, 'Password changed successfully')
            return HttpResponseRedirect('/pro/')
    else:
        fm = SetPasswordForm(user=request.user)
    return render(request, 'forgotpass.html', {'form':fm})

def donate_us(request):
    if request.user.is_authenticated :
        if request.method == 'POST':
            fm = donateForm(instance=request.user)
            data_dict = {
            'MID':'mvWQDv43556208598369',
            'ORDER_ID':'dddgfgfeeed',
            'TXN_AMOUNT':'1',
            'CUST_ID':'email',
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
	        'CALLBACK_URL':'http://localhost:8000/handlerequest/',
            # mvWQDv43556208598369
            }
            return render(request, 'paytm.html', {'data_dict':data_dict})
        else:
            fm = donateForm(instance=request.user)    
            return render(request, 'donate.html', {'form':fm})
    else:
        return HttpResponseRedirect('/login/')

@csrf_exempt
def handleRequest(request):
    return HttpResponse('Done')    


r = requests.get("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN&ceid=IN%3Aen")
# r = requests.get("https://news.google.co.in")
soup = BeautifulSoup(r.content, 'html.parser')
titles  = []
images = []
links = []
for x in soup.find_all('div', attrs={'jsname':'gKDw6b'}):
    links.append("https://news.google.co.in" + x.find('a').get('href'))
for x in soup.find_all('img', class_="""tvs3Id QwxBBf"""):
    images.append(x.get('src'))
for x in soup.find_all('h3', class_="""ipQwMb ekueJc RD0gLb"""):
    titles.append(x.text)
news = list(zip(titles, images, links))
jnews = json.dumps(news)

def pro_page(request):
    if request.user.is_authenticated:
        return render(request, 'pro.html', {'name':request.user, 'news':news})   #'toi_news':toi_news
    else:
        return HttpResponseRedirect('/login/')    

# ind_r = requests.get("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pKVGlnQVAB/sections/CAQiSENCQVNNQW9JTDIwdk1EVnFhR2NTQldWdUxVZENHZ0pKVGlJT0NBUWFDZ29JTDIwdk1ETnlhekFxQ1FvSEVnVkpibVJwWVNnQSouCAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JXVnVMVWRDR2dKSlRpZ0FQAVAB?hl=en-IN&gl=IN&ceid=IN%3Aen")
# ind_soup = BeautifulSoup(ind_r.content, 'html.parser')
# ind_titles  = []
# ind_images = []
# ind_links = []
# for x in ind_soup.find_all('div', attrs={'jsname':'gKDw6b'}):
#     ind_links.append("https://news.google.co.in" + x.find('a').get('href'))
# for x in ind_soup.find_all('img', class_="""tvs3Id QwxBBf"""):
#     ind_images.append(x.get('src'))
# for x in ind_soup.find_all('h3', class_="""ipQwMb ekueJc RD0gLb"""):
#     ind_titles.append(x.text)
# ind_news = list(zip(ind_titles, ind_images, ind_links))

# # print(ind_news)
ind_news = []
def indNews(request):
    if request.user.is_authenticated:
        return render(request, 'indnews.html', {'name':request.user, 'ind_news':ind_news})   #'toi_news':toi_news
    else:
        return HttpResponseRedirect('/login/')        

# wrd_r = requests.get("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pKVGlnQVAB/sections/CAQiSENCQVNNQW9JTDIwdk1EVnFhR2NTQldWdUxVZENHZ0pKVGlJT0NBUWFDZ29JTDIwdk1EbHViVjhxQ1FvSEVnVlhiM0pzWkNnQSouCAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JXVnVMVWRDR2dKSlRpZ0FQAVAB?hl=en-IN&gl=IN&ceid=IN%3Aen")
# wrd_soup = BeautifulSoup(wrd_r.content, 'html.parser')
# wrd_titles  = []
# wrd_images = []
# wrd_links = []
# for x in wrd_soup.find_all('div', attrs={'jsname':'gKDw6b'}):
#     wrd_links.append("https://news.google.co.in" + x.find('a').get('href'))
# for x in wrd_soup.find_all('img', class_="""tvs3Id QwxBBf"""):
#     wrd_images.append(x.get('src'))
# for x in wrd_soup.find_all('h3', class_="""ipQwMb ekueJc RD0gLb"""):
#     wrd_titles.append(x.text)
# wrd_news = list(zip(wrd_titles, wrd_images, wrd_links))
wrd_news = []

def wrdNews(request):
    if request.user.is_authenticated:
        return render(request, 'worldnews.html', {'name':request.user, 'wrd_news':wrd_news})   #'toi_news':toi_news
    else:
        return HttpResponseRedirect('/login/')  

def get_html_content(sear):
    # print(sear)
    # s = sear['sear'].strip()
    x = sear.replace(' ', "%20")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    u = 'https://news.google.com/search?q='+x+'&hl=en-IN&gl=IN&ceid=IN%3Aen'
    return u

def search(request):
    sear_news = []
    # print(request.GET.get('search'))
    if 'search' in request.GET:
        sear = get_html_content(request.GET.get('search'))
        print(sear)
        sear_r = requests.get(sear)
        sear_soup = BeautifulSoup(sear_r.content, 'html.parser')
        sear_titles  = []
        sear_images = []
        sear_links = []
        for x in sear_soup.find_all('div', class_="xrnccd"):
            sear_links.append("https://news.google.co.in" + x.find('a').get('href'))
            print('1')
        for x in sear_soup.find_all('img', class_="""tvs3Id QwxBBf"""):
            sear_images.append(x.get('src'))
            print('2')
        for x in sear_soup.find_all('h3', class_="""ipQwMb ekueJc RD0gLb"""):
            print('3')
            sear_titles.append(x.text)    
        sear_news = list(zip(sear_titles, sear_images, sear_links))
        # print(*sear_news)
    return render(request, 'search.html', {'sear_news':sear_news})  
