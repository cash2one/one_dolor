#coding=utf-8
import hashlib
import json
# from lxml import etree
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from wechatpy import WeChatClient
from yiyuanduobao_shop.models import *
from weixin import handler as HD
from weixin.backends.dj import Helper, sns_userinfo
from weixin import WeixinHelper, JsApi_pub, WxPayConf_pub, UnifiedOrder_pub,Redpack_pub, Notify_pub, catch
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
import json
# Create your views here.
conf_instance = WechatConf(
    token=WxPayConf_pub.TOKEN, 
    appid=WxPayConf_pub.APPID, 
    appsecret=WxPayConf_pub.APPSECRET,
    encrypt_mode='normal')
wechat_instance=WechatBasic(conf_instance)


@csrf_exempt
def do(request):
	# access token 记录在session中
	if 'access_token' not in request.session:
		request.session['access_token'] = fetch_access_token()
	"""公众平台对接"""
	signature = request.REQUEST.get("signature", "")
	timestamp = request.REQUEST.get("timestamp", "")
	nonce = request.REQUEST.get("nonce", "")
	if not any([signature, timestamp, nonce]) or not WeixinHelper.checkSignature(signature, timestamp, nonce):
		return HttpResponse("check failed")
	if request.method == "GET":
		return HttpResponse(request.GET.get("echostr"))
	elif request.method == "POST":
		global wechat_instance
		parse_message = wechat_instance.parse_data(data=request.body)
		response = event_dispatch(wechat_instance)
		# handler = HD.MessageHandle(request.body)
		# response = handler.start()
		return HttpResponse(response)
	else:
		return HttpResponse("")


def event_dispatch(message):
	response = ""
	if wechat_instance.message.type == 'subscribe':
		key = wechat_instance.message.key
		ticket = wechat_instance.message.ticket
		response = subscribe(key,ticket)
	elif wechat_instance.message.type == 'unsubscribe':
		response = unsubscribe()
	elif wechat_instance.message.type == 'click':
		key = wechat_instance.message.key
		response = click(wechat_instance,key)
	return response


# 关注事件
def subscribe(key,ticket):
	response = "欢迎关注一元夺宝，这里会持续出品给您创富的项目！"
	return response 

# 取消关注事件
def unsubscribe():
	response = "取消关注"
	return response

# 点击事件
def click(wechat_instance,key):
	print "click event!"
	response = None
	if key == "V1001_TODAY_DUOBAO_SHOP": # 开夺宝店
		articles = [{
				'title': u'免费入驻桔叶夺宝分店，拥有自己的夺宝分店，踏上2016创富之路！',
				'description': u'免费入驻，超高回报！',
				'picurl': u'http://2.juye51.com/media/imgs/money.jpg',
				'url': u'http://mp.weixin.qq.com/s?__biz=MzI0NzE3NTUwMA==&mid=502871956&idx=1&sn=332539af7c5a9052ce153b80ef16d285&scene=0#wechat_redirect',
			}]
		response = wechat_instance.response_news(articles)
	return response


# 获取access token
def fetch_access_token():
	appid = WxPayConf_pub.APPID
	appsecret = WxPayConf_pub.APPSECRET
	client = WeChatClient(appid, appsecret)
	return client.fetch_access_token()['access_token']
