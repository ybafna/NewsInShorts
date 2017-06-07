import json
from urllib.request import urlopen,Request
from django.shortcuts import render
from django.http import HttpResponse
import ssl
import operator

from django.utils.timezone import activate

from NewsInShorts import settings
from .models import News,Source
import requests
from datetime import datetime
from django.contrib.auth.models import User
from getnews.models import UserProfile
import json
from urllib.request import urlopen,Request
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.views.generic import View
from django.http import HttpResponse
from .models import News,Source
from django.contrib.auth.models import User
from getnews.models import UserProfile
import requests
from multiprocessing import Pool




#activate(settings.TIME_ZONE)

# Create your views here.
def index(request):
    #getSource(request)
    pool = Pool(processes=100)  # process per core
    #pool.map(getAllNews(request))
    #return HttpResponse("SUCCESS")
    #getAllNews(request)
    allNews = News.objects.all()
    allSource = Source.objects.all()
    return render(request, 'getnews/accordion.html', {'allNews':allNews,'allSource':allSource})
    '''
    abcd = ""
    for news in searchNews:
        abcd = abcd + news.title + "__"+ news.source.name +"<br>"
    return HttpResponse(abcd)'''
'''class Counter:
    counter = 0

    def increment(self):
        self.counter += 1
    def set_to_zero(self):
        self.counter = 0
'''
#context['loop_times'] = range(1, 8)

def trending(request):
    generalNews  = getCategoryNews('general')[0:9]
    sportNews = getCategoryNews('sport')[0:9]
    businessNews = getCategoryNews('business')[0:9]
    entertainmentNews = getCategoryNews('entertainment')[0:9]
    scienceAndNatureNews = getCategoryNews('science-and-nature')[0:9]
    technologyNews = getCategoryNews('technology')[0:9]
    context = {
        'generalNews': generalNews,
        'sportNews' : sportNews,
        'businessNews':businessNews,
        'entertainmentNews':entertainmentNews,
        'scienceAndNatureNews':scienceAndNatureNews,
        'technologyNews':technologyNews,

    }
    return render(request,'getnews/trendingTemplate.html',context)

def paper(request,paper_id):
    paperSource = Source.objects.get(pk=paper_id)
    paperNews = getImageNews(paperSource.source_id)
    context = {
        'paperNews': paperNews,
        'paperNewsTop': paperNews[0:6]
    }
    return render(request,'getnews/paperTemplate.html',context)

def getSource(request):
    for source in Source.objects.all():
        Source.objects.get(id=source.id).delete()
    url = "https://newsapi.org/v1/sources?language=en"
    r =requests.get(url)
    sources = r.json()['sources']
    for source in sources:
        s = Source()
        s.source_id = source["id"]
        s.name = source["name"]
        s.description = source["description"]
        s.url = source["url"]
        categoryStr = source["category"]
        if(categoryStr is 'science-and-nature'):
            categoryStr = 'science_nature'
        s.category=categoryStr
        s.country = source["country"]
        s.urlsToLogos_large = source["urlsToLogos"]["large"]
        s.urlsToLogos_medium = source["urlsToLogos"]["medium"]
        s.urlsToLogos_small = source["urlsToLogos"]["small"]
        s.save()

def getAllNews(request):
    for news in News.objects.all():
        News.objects.get(id=news.id).delete()
    sources = Source.objects.all()
    for source in sources:
        articles = ""
        try:
            url = 'https://newsapi.org/v1/articles?source='+source.source_id+'&apiKey=d98bbacb46d94dde9d40ce02e5d7cf7a'
            r = requests.get(url)
            articles = r.json()['articles']
        except:
            pass

        for article in articles:
            news = News()
            news.author = article["author"]
            news.title = article["title"]
            news.description = article["description"]
            news.url = article["url"]
            news.urlToImage = article["urlToImage"]
            dateString = article["publishedAt"]

            try:
                dateString = dateString[0:19]
                news.publishedDate = datetime.strptime(dateString, "%Y-%m-%dT%H:%M:%S")
            except:
                pass
            news.source = source
            news.save()


def category(request):
    url =  request.get_full_path()
    urls =url.split('/')
    #return HttpResponse(urls[2])
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        u = UserProfile.objects.get(user=request.user)
        at=getattr(u,urls[2])
        at=at+1
        setattr(u, urls[2], at)
        u.save()


    categoryNews = getCategoryNews(urls[2])
    context = {
        'paperNews': categoryNews,
        'paperNewsTop': categoryNews[0:6]
    }
    return render(request,'getnews/paperTemplate.html',context)

def getImageNews(sourceStr):
    allNews = News.objects.all()
    validImageNews = []
    for news in allNews:
        if news.source.source_id in [sourceStr] and news.urlToImage:
            validImageNews.append(news)
    return validImageNews

def getCategoryNews(cat):
    allSource = Source.objects.all().filter(category=cat)
    allNews = News.objects.all().filter(source__in=allSource).order_by('-publishedDate')
    categoryNews = []
    for news in allNews:
        if news.urlToImage:
            categoryNews.append(news)
    return categoryNews


def search(request):
    keywordNews = []
    keyword=request.POST['keyword']
    keywords = keyword + ""
    keywordString = keywords.split(',')

    allNews = News.objects.all()
    for news in allNews:
        titleString = news.title.split(' ')
        for s in titleString:
            if s in keywordString:
                keywordNews.append(news)

    context = {
        'keywordNews': keywordNews,
        'keyword':keyword
    }

    return render(request,'getnews/searchTemplate.html',context)

def logincheck(request):
    allNews = News.objects.all()
    allSource = Source.objects.all()
    if request.user.is_authenticated:
        u = UserProfile.objects.get(user=request.user)
        if ((u.sport == 0 and u.general == 0) and (u.business == 0 and u.technology == 0)) and (
                u.science_nature == 0 and u.entertainment == 0):
            return render(request, 'getnews/accordion.html', {'allNews': allNews, 'allSource': allSource})
        else:
            list = {'sport': u.sport, 'general': u.general, 'business': u.business, 'technology': u.technology,
                    'science_nature': u.science_nature, 'entertainment': u.entertainment}
            large = max(list, key=list.get)
            return redirect(large)

