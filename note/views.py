from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from .models import Note
def check_login(fn):
    def wrap(request,*args,**kwargs):
        if 'username' not in request.session or 'uid' not in request.session:
            c_username = request.COOKIES.get('username')
            c_uid = request.COOKIES.get('uid')
            if not c_username or not c_uid:
                return HttpResponseRedirect('/user/login')
            else:
                request.session['username'] = c_username
                request.session['uid'] = c_uid
        return fn(request,*args,**kwargs)
    return wrap

# Create your views here.
@check_login
def add_note(request):

    if request.method=='GET':
        return render(request,'note/add_note.html')
    elif request.method=='POST':
        uid = request.session['uid']
        title = request.POST['title']
        content = request.POST['content']

        Note.objects.create(title=title,content=content,user_id=uid)
        return HttpResponseRedirect('/note/list_note')

@check_login
def list_note(request):
    uid = request.session['uid']
    note=Note.objects.filter(user_id=uid)

    return render(request,'note/list_note.html',locals())

@check_login
@cache_page(120)
def page_note(request,note_id):
    uid = request.session['uid']
    try:
        content=Note.objects.get(id=note_id,user_id=uid)
        title=content.title
        content=content.content
    except Exception as e:
        return HttpResponse('找不到页面呢呜呜呜')
    return render(request,'note/page_note.html',locals())