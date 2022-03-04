from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User
import hashlib
# Create your views here.
def reg_view(request):
    #注册
    if request.method=='GET':
        return render(request,'user/register.html')
    elif request.method=='POST':
        username=request.POST['username']
        password1=request.POST['password_1']
        password2=request.POST['password_2']

    #GET 返回页面
    #POST
    # 1、密码一致
        if password1 != password2:
            return HttpResponse('密码不一致')
        m = hashlib.md5()
        m.update(password1.encode())
        password_m=m.hexdigest()
    # 2、用户名是否可用
        old_user = User.objects.filter(username=username)
        if old_user:
            return HttpResponse('已存在的用户名')
    # 3、插入数据
        try:
            user=User.objects.create(username=username,password=password_m)
        except Exception as e:
            print('人太多咯')
            return HttpResponse('已存在的用户名')
    # 7day免密登录
        request.session['username'] = username
        request.session['uid']=user.id

        return HttpResponseRedirect('/index')

def login_view(request):
    if request.method=='GET':
        # 检查登录状态
        if request.session.get('username') and request.session.get('uid'):
            return HttpResponseRedirect('/index')
        c_username= request.COOKIES.get('username')
        c_uid= request.COOKIES.get('uid')
        if c_uid and c_username:
            request.session['username']=c_username
            request.session['uid']=c_uid
            return HttpResponseRedirect('/index')
        return render(request,'user/login.html')
    elif request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print(f'已存在用户名 {e}')
            return HttpResponse('用户名或密码不正确')

        m=hashlib.md5()
        m.update(password.encode())
        if m.hexdigest() != user.password:
            return HttpResponse('用户名或密码不正确')

        request.session['username']=username
        request.session['uid']=user.id

        resp = HttpResponseRedirect('/index')
        if 'remember' in request.POST:
            resp.set_cookie('username',username,3600*24*3)
            resp.set_cookie('uid',user.id,3600*24*3)

        return resp

def logout_view(request):
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
    resp = HttpResponseRedirect('/index')
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')
    return resp