#coding=utf-8
from django.db import models

# Create your models here.

class Customer(models.Model):
	openid = models.CharField(max_length=255,default="",blank=True,null=True,verbose_name="微信openid")
	playtimes = models.IntegerField(default=3,blank=True,null=True,verbose_name="可以玩的次数")