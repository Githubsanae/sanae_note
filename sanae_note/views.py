import os.path

from django.conf import settings
from django.core import mail
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from upload_app.models import Content

def test_page(request):
    #/test_page?page=1
    page_num = request.GET.get('page',1)
    all_data=['koishi','yukari','shiroko','sanae','satori','nonomi','hatsune','neneka','pekorimu','kokkoro','reimu','marisa']
    p=Paginator(all_data,3)
    c_page=p.page(int(page_num))
    return render(request,'test_page.html',locals())

@csrf_exempt
def test_upload(request):
    if request.method == 'GET':
        return render(request,'test_upload.html')
    elif request.method == 'POST':

        # files=request.FILES['myfile']
        # filename= os.path.join(settings.MEDIA_ROOT,files.name)
        # with open(filename,'wb') as f:
        #     data=files.file.read()
        #     f.write(data)

        files=request.FILES['myfile']
        title=files.name
        Content.objects.create(title=title,picture=files)
        return HttpResponse(f'文件上传成功{title}')

@csrf_exempt
def test_mail(request):
    if request.method =='GET':
        return render(request,'test_mail.html')
    elif request.method =='POST':
        subject=request.POST['subject']
        content=request.POST['content']
        print(subject)
        print(content)
        mail.send_mail(subject=subject,message=content,from_email='2424252675@qq.com',recipient_list=['wufan20011207@gmail.com','2424252675@qq.com'])
        print('send')
        return HttpResponse('发送成功')