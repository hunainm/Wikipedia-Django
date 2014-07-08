from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from rest_framework import viewsets, routers
from datetime import datetime
from wiki import serializers
from django.db.models import Q


# Create your views here.
from wiki.models import Page, PageHistory,PagePrivacy,Notifications


def editor(request):
    c = {}
    c.update(csrf(request))
    c['request']=request
    return render_to_response('NewPage.html',c)

def CreatePage(request):
    c={}
    c.update(csrf(request))
    c['request']=request
    if request.method == 'POST':  # If the form has been submitted...
            form = Page()
            form.title=request.POST['title']
            form.content=request.POST['content']
            form.admin=request.user
            privacy=PagePrivacy.objects.get(Type=request.POST['type'])
            form.Privacy=privacy
            Title=request.POST['title']
            if Page.objects.filter(title=Title):
                c['errors']="Page already Exists"
                c['content']=request.POST['content']
                return HttpResponseRedirect('/wiki/',c)
            else:
                form.save()
                c.update(csrf(request))
                c['form'] = form
                return HttpResponseRedirect('/wikipedia/', c)



def HomePage(request):
    c = {}
    c.update(csrf(request))
    c["request"]=request
    if request.user.is_authenticated():
                notifications= Notifications.objects.filter(user=request.user.id)
                c['number']=notifications.count()
                c['notifications'] = notifications

    if request.method == 'POST':
        if request.POST['search'] != '':
            return HttpResponseRedirect('/wikipedia/wiki/' + request.POST['search'])
        else:
            return render_to_response('wikipedia.html', c)
    else:
        return render_to_response('wikipedia.html', c)

def ShowModifiedPage(request,page_name):
    c = {}
    c.update(csrf(request))
    c['request']=request
    try:
        c['data'] = Page.objects.get(title=page_name)
    except Page.DoesNotExist:
        c['data'] = None

    if c['data'] is None:
        return HttpResponseRedirect('/404/')
    else:
        if request.user.is_authenticated():
            notifications=Notifications.objects.filter(user=request.user.id)
            c['number']=notifications.count()
            c['notifications']=notifications
        return render_to_response('ModifiedPage.html', c)

def ShowHistoryPage(request):
    c={}
    c.update(csrf(request))
    c['request']=request
    pTitle=request.GET['title']
    changeID=request.GET['id']
    page = Page.objects.get(title=pTitle)
    c['data'] = page
    c['history'] = PageHistory.objects.get(Page=page.id,id=changeID)
    if request.user.is_authenticated():
            notifications=Notifications.objects.filter(user=request.user.id)
            c['number']=notifications.count()
            c['notifications']=notifications

    return render_to_response('HistoryPage.html', c)


def ShowHistoryList(request):
    c={}
    c.update(csrf(request))
    c['request']=request
    pTitle=request.GET['title']
    page = Page.objects.get(title=pTitle)
    c['data'] = page
    c['history'] = PageHistory.objects.filter(Page=page.id)
    if request.user.is_authenticated():
            notifications=Notifications.objects.filter(user=request.user.id)
            c['number']=notifications.count()
            c['notifications']=notifications

    return render_to_response('ShowHistory.html', c)


def ShowSearchPage(request, page_name):
    c = {}
    c['request']=request
    try:
        c['data'] = Page.objects.get(title=page_name)
    except Page.DoesNotExist:
        c['data'] = None

    if c['data'] is None:
        return HttpResponseRedirect('/404/')
    else:
        if request.user.is_authenticated():

            notifications=Notifications.objects.filter(user=request.user.id)
            c['number']=notifications.count()
            c['notifications']=notifications

        return render_to_response('wiki.html', c)

def PageNotFound(request):
    return render_to_response('404.html')


def DeletePage(request):
    c = {}
    c.update(csrf(request))
    c['request']=request
    s = request.GET['title']
    if s != '':
            if Page.objects.get(title=s):
                Page.objects.get(title=s).delete()
                c['success'] = "Your page has been deleted"
                return HttpResponseRedirect('/wikipedia/')
            else:
                c['success'] = "Page not found"
                return HttpResponseRedirect('/wikipedia/')
    else:
            c['success'] = ""
            return HttpResponseRedirect('/wikipedia/')

def editPage(request):
    c={}
    c.update(csrf(request))
    c['request']=request
    Title=request.GET['title']
    c['data'] = Page.objects.filter(title=Title)
    notifications=Notifications.objects.filter(user=request.user.id)
    c['number']=notifications.count()
    c['notifications']=notifications

    return render_to_response('EditPage.html',c)

def acceptChanges(request):
    c={}
    c.update(csrf(request))
    c['request']=request
    Title=request.GET['title']
    x=Page.objects.get(title=Title)
    if request.POST['accept']=='true':
        y=PageHistory()
        y.History=x.content
        y.Page=x
        y.Modifier=request.user
        y.save()
        x.content=x.ModifiedContent
        x.ModifiedContent=''
        x.ModifyRequest=False
        x.modifyDate=datetime.now()
        x.save()

    else:
        x.ModifiedContent=''
        x.ModifyRequest=False
        x.save()

    return HttpResponseRedirect('/wikipedia/wiki/' + request.GET['title'])

def EditPage(request):
      if request.method== 'POST':
            x=Page.objects.get(title=request.POST['title'])
            if x.admin.id != request.user.id:
                if x.Privacy.Type=='public':
                    y=PageHistory()
                    y.History=x.content
                    y.Page=x
                    y.Modifier=request.user
                    y.save()
                    x.content=request.POST['content']
                    x.modifyDate=datetime.now()
                    x.save()
                    z=Notifications()
                    z.user=x.admin
                    z.message="Your page '" + x.title + "' has been modified."
                    z.link="/wikipedia/wiki/"+x.title
                    z.article=x
                    z.save()
                    request.session['changeStatus'] = "The changes in content have been saved"


                elif x.Privacy.Type=='semi private':
                    x.ModifiedContent=request.POST['content']
                    x.ModifyRequest=True
                    x.save()
                    z=Notifications()
                    z.user=x.admin
                    z.message="Your page '" + x.title + "' has been modified. Review the changes."
                    z.link="/wikipedia/wiki/changes/"+x.title
                    z.article=x
                    z.save()

                    request.session['changeStatus'] = "The changes will be reviewed by page admin before being saved"

            else:
                y=PageHistory()
                y.History=x.content
                y.Page=x
                y.Modifier=request.user
                y.save()
                x.content=request.POST['content']
                x.save()
                request.session['changeStatus'] = "The changes in content have been saved"


            return HttpResponseRedirect('/wikipedia/wiki/' + request.POST['title'])

def NewAccount(request):
    c={}
    c.update(csrf(request))
    c['request']=request

    if request.method == 'POST':
        if User.objects.filter(username=request.POST['username']):
            c['UsernameError']="Username already Exists"
            return render_to_response('CreateAccount.html',c)
        else:
            if request.POST['password'] != request.POST['pwRetype']:
                c['UsernameError']="The passwords donot match. Please type again"
                return render_to_response('CreateAccount.html',c)
            else:
                user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
                user.save()
                return HttpResponseRedirect('/login/', c)

def CreateAccount(request):
    c={}
    c.update(csrf(request))
    c['request']=request
    return render_to_response('CreateAccount.html',c)

def Login(request):
    c={}
    c.update(csrf(request))
    c['request']=request
    return render_to_response('Login.html',c)

def authenticateUser(request):
    c={}
    c.update(csrf(request))
    c['request']=request
    username = request.POST['username']
    password = request.POST['password']
    if User.objects.filter(username=username):
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            c['request']=request
            return HttpResponseRedirect('/wikipedia/',c)

        else:
            c['error']="Your username and password didn't match"
            return render_to_response('Login.html',c)
    else:
        c['error']="The username does not exist"
        return render_to_response('Login.html',c)

def Logout(request):
    logout(request)
    c={}
    c.update(csrf(request))
    c['request']=request
    return HttpResponseRedirect('/wikipedia/',c)


def SearchAcrossPages(request):
    c={}
    c.update(csrf(request))
    c['request']=request
    if request.user.is_authenticated():
            notifications=Notifications.objects.filter(user=request.user.id)
            c['number']=notifications.count()
            c['notifications'] = notifications

    keyword=request.GET['searchWord']
    c['search']= Page.objects.filter(content__contains=keyword)

    return render_to_response('SearchPage.html',c)

def SearchAcrossTitles(request):
    c={}
    c.update(csrf(request))
    c['request']=request
    if request.user.is_authenticated():
            notifications=Notifications.objects.filter(user=request.user.id)
            c['number']=notifications.count()
            c['notifications'] = notifications

    keyword=request.POST['search']
    page= Page.objects.filter(title__contains=keyword)
    c['search']=page
    return render_to_response('SearchPage.html',c)

def Contributions(request):
    c={}
    c.update(csrf(request))
    c['request']=request
    if request.user.is_authenticated():
            notifications=Notifications.objects.filter(user=request.user.id)
            c['number']=notifications.count()
            c['notifications'] = notifications

    id=request.GET['id']
    page = Page.objects.filter(admin=id)
    c['search']= page
    c['contribute']=True
    c['username']= request.user.username

    return render_to_response('SearchPage.html',c)

def ViewAllNotifications(request):
    c={}
    c.update(csrf(request))
    c['request']=request
    if request.user.is_authenticated():
            notifications = Notifications.objects.filter(user=request.user.id)
            c['number']=notifications.count()
            c['notifications'] = notifications

    id=request.GET['id']
    notify = Notifications.objects.filter(user=id)
    c['search']= notify
    c['notify'] = True
    c['username']= request.user.username

    return render_to_response('SearchPage.html',c)


class PageViewSet(viewsets.ModelViewSet):

    queryset = Page.objects.all()
    serializer_class = serializers.PageSerializer
