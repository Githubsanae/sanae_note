from django.db import models

# Create your models here.
class Content(models.Model):
    title= models.CharField('名字',max_length=50)
    picture=models.FileField(upload_to='picture')