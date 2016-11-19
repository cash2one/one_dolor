#coding=utf-8
from django.shortcuts import render
from django.shortcuts import HttpResponse, render_to_response, redirect
import urllib,urllib2,json,time,datetime
from yiyuanduobao_shop.models import Shop,ShopManager,Customer,Merchant,Item,Order
# Create your views here.



def session_test(request):
	response = {}
	if 'h' in request.session:
		print request.session['h']
	else:
		print "not in"
	request.session['h'] = 222
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))


########################################
#
# 	API 接口
#
########################################

def fetch_all_items(request):
	response = {}
	items = Item.objects.filter(item_status=0)
	response['code'] = 0
	response['items'] = items
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

