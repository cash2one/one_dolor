#coding=utf-8
from django.shortcuts import render
from django.shortcuts import HttpResponse, render_to_response, redirect
from django.http import HttpResponseRedirect
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from weixin import handler as HD
from weixin.backends.dj import Helper, sns_userinfo
from weixin import WeixinHelper, JsApi_pub, WxPayConf_pub, UnifiedOrder_pub,Redpack_pub, Notify_pub, catch
from wechatpy import WeChatClient
from market_game_draw_circle.models import *
import random
import urllib,urllib2,json,time,datetime

@sns_userinfo
def index(request):
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	current_url = "http://2.juye51.com" +request.get_full_path()
	request.session['game_url'] = current_url	
	# 查找是否有此用户
	current_customers = Customer.objects.filter(openid=request.session['openid'])
	current_customer = None
	if len(current_customers) == 0:
		current_customer = Customer.objects.create(openid=request.session['openid'])
	else:
		current_customer = current_customers[0]
	if 'score' in request.GET:
		score = float(request.GET['score'])
		desc = request.GET['desc']
		current_customer.playtimes -= 1
		current_customer.save()
		current_playtimes = current_customer.playtimes
		return render(request,'web/draw_circle_result.html',{'score':score,'desc':desc,'current_playtimes':current_playtimes})
	else:
		return render(request,'web/draw_circle.html')

def result(request):
	request.session['score'] = request.GET['score']
	request.session['desc'] = request.GET['desc']
	return render(request,'web/draw_circle_result.html')	

def resultpage(request):
	score = float(request.GET['score'])
	desc = request.GET['desc']
	return render(request,'web/draw_circle_result.html')	


# 分享微信

@csrf_exempt
@catch
def share_game(request):
	if 'openid' in request.session['openid']:
		openid = request.session['openid']
		try:
			customer = Customer.objects.get(openid=openid)
			customer.playtimes += 3
			customer.save()
			print customer.playtimes
		except:
			print "no such customer"
	share_issue_result = {}
	share_issue_result['share_desc'] = "6.1快乐！画个圆赢取红包啦"
	share_issue_result['share_title'] = "6.1快乐！画个圆赢取红包啦"
	share_issue_result['urllink'] = "http://2.juye51.com/game/draw_circle/"
	share_issue_result['share_imgpath'] = "http://juye-yiyuanduobao.oss-cn-beijing.aliyuncs.com/icon.png"
	return HttpResponse(json.dumps(share_issue_result))	

# 获取jsapi signature方法
@csrf_exempt
@catch
def get_jsapi_signature(request):
    print "get_onedolor_jsapi_signature !!"
    wechatpy_client = fetch_wechatpy_client()
    js_api_ticket = wechatpy_client.jsapi.get_jsapi_ticket() # 获取js_api_ticket
    # 生成noncestr
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    strs = []
    length = 32
    for x in range(length):
        strs.append(chars[random.randrange(0, len(chars))])
    noncestr = "".join(strs)
    # 生成timestamp
    timeStamp = int(time.time())
    current_url = request.session['game_url']
    print "current_url = ",current_url
    # 生成当前参数字典
    current_params_dict = {'jsapi_ticket':js_api_ticket,'noncestr':noncestr,'timestamp':timeStamp,'url':current_url}
    # current_params_str = urllib.urlencode(current_params_dict)
    current_params_str = "jsapi_ticket=%s&noncestr=%s&timestamp=%s&url=%s" % (js_api_ticket,noncestr,timeStamp,current_url)
    import hashlib
    signature = hashlib.sha1(current_params_str).hexdigest()
    signature_result = {'appid':WxPayConf_pub.APPID,'appsecret':WxPayConf_pub.APPSECRET,
    'signature':signature,'noncestr':noncestr,
    'jsapi_ticket':js_api_ticket,'timestamp':timeStamp,'url':current_url}
    # print signature_result
    return HttpResponse(json.dumps(signature_result))


# 获取access token
def fetch_access_token():
	appid = WxPayConf_pub.APPID
	appsecret = WxPayConf_pub.APPSECRET
	client = WeChatClient(appid, appsecret)
	return client.fetch_access_token()['access_token']

# 获取wechat的client
def fetch_wechatpy_client():
	appid = WxPayConf_pub.APPID
	appsecret = WxPayConf_pub.APPSECRET
	client = WeChatClient(appid, appsecret)
	return client