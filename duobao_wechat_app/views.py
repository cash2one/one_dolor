#coding=utf-8
from django.shortcuts import render
from django.shortcuts import HttpResponse, render_to_response, redirect
from django.http import HttpResponseRedirect
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
import urllib,urllib2,json,time,datetime
from yiyuanduobao_shop.models import *
from weixin import handler as HD
from weixin.backends.dj import Helper, sns_userinfo
from weixin import WeixinHelper, JsApi_pub, WxPayConf_pub, UnifiedOrder_pub,Redpack_pub, Notify_pub, catch
from django.db import transaction
import random
from wechatpy import WeChatClient
from bs4 import BeautifulSoup
import logging
import re


MEDIA_URL = "/media/"
FAIL, SUCCESS = "FAIL", "SUCCESS"
# 首页
def index(request):
	logger = logging.getLogger('default')
	# 获取shop_id
	shop_id = None
	if 'shop_id' in request.GET:
		shop_id = request.GET['shop_id']
	elif 'shop_id' in request.session:
		shop_id = request.session['shop_id']
	shop = Shop.objects.get(id=shop_id)
	# page_id = 1
	# page_length = 50
	# if "page_id" in request.GET:
	# 	page_id = int(request.GET['page_id'])
	# elif "page_id" in request.POST:
	# 	page_id = int(request.POST['page_id'])

	# if "page_length" in request.GET:
	# 	page_length = int(request.GET['page_length']) 
	# elif "page_length" in request.POST:
	# 	page_length = int(request.POST['page_length'])
	# request.session['last_login_shop_id'] = shop_id
	shop_banners = ShopBanner.objects.filter(shop=shop)
	if len(shop_banners) == 0:
		shop_banners = ShopBanner.objects.filter(shop__id=1)
	# 查看session购物车的内容
	cart_list = {}
	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']	
	cart_good_number = 0
	new_cart_list = {} # 过滤后的购物车
	for item_id in cart_list:
		try:
			item = Item.objects.get(id=item_id)
		except:
			continue
		if int(item.merchant.shop_id) != int(shop_id):
			continue
		print new_cart_list
		if item_id in new_cart_list:
			new_cart_list[item_id] += cart_list[item_id]
		else:
			new_cart_list[item_id] = cart_list[item_id]
		cart_good_number += cart_list[item_id]

	request.session['cart_list'] = new_cart_list
	# 将session中的message置为已读
	my_have_read_message_list = []
	if 'message_list' in request.session:
		my_have_read_message_list = request.session['message_list']

	for message_id in my_have_read_message_list:
		my_have_read_message = NoticeMsg.objects.get(id=int(message_id))
		my_have_read_message.notice_msg_status_id = 2
		my_have_read_message.save()
	request.session['message_list'] = []	# 置空消息		
	# 消息置为已读结束

	# 获取所有进行中的期的数据
	progressing_items = Item.objects.filter(merchant__shop__id=shop_id,item_status_id=1,proxy_sale_customer=None) # 进行中的
	# 筛选出显示的期
	filter_items = progressing_items
	filter_item_infos = {}
	for item in filter_items:
		temp_iteminfo = {}
		if item.merchant.mer_type_id == 3:
			temp_iteminfo['surplus'] = item.merchant.price - item.take_part_num
			temp_iteminfo['take_part_price'] = item.take_part_num
		else:
			temp_iteminfo['surplus'] = item.merchant.price - item.take_part_num
			temp_iteminfo['take_part_price'] = item.take_part_num	
		temp_iteminfo['progress'] = "%.1f" % (float(temp_iteminfo['take_part_price'])/float(item.merchant.price) * 100.0)
		filter_item_infos[item] = temp_iteminfo

		
	return render(request,'web/index.html',{'cart_good_number':cart_good_number,"filter_item_infos":filter_item_infos,
		"shop_id":shop_id,"shop":shop,"shop_banners":shop_banners})

###############################################################
#
#             商店模块
# 
###############################################################

# 十元专区 
@sns_userinfo
def ten_yuan(request):
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']
	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 	
	# 获取用户
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	shop_id = request.GET['shop_id']
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)		
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
		logger = logging.getLogger('default')
		logger.info("[新用户] 进入10元专区，新增用户 %s !" % nickname)		

	else:
		customer = customers[0]
		account = customer.account
	# 只要
	items = Item.objects.filter(merchant__mer_type_id=3,merchant__shop_id=shop_id,item_status_id=1) # 红包专区item
	iteminfo = {}
	for item in items:
		temp_iteminfo = {}
		if item.merchant.mer_type_id == 3:
			temp_iteminfo['surplus'] = item.merchant.price - item.take_part_num
			temp_iteminfo['take_part_price'] = item.take_part_num 
		else:
			temp_iteminfo['surplus'] = item.merchant.price - item.take_part_num
			temp_iteminfo['take_part_price'] = item.take_part_num

		iteminfo[item] = temp_iteminfo
	

	# 查看session购物车的内容
	cart_list = {}
	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']	
	cart_good_number = 0
	# new_cart_list = {} # 过滤后的购物车
	for item_id in cart_list:
		item = Item.objects.get(id=item_id)
		if int(item.merchant.shop_id) != int(shop_id):
			continue
		cart_good_number += cart_list[item_id]		

	# 将session中的message置为已读
	my_have_read_message_list = []
	if 'message_list' in request.session:
		my_have_read_message_list = request.session['message_list']

	for message_id in my_have_read_message_list:
		my_have_read_message = NoticeMsg.objects.get(id=int(message_id))
		my_have_read_message.notice_msg_status_id = 2
		my_have_read_message.save()
	request.session['message_list'] = []	# 置空消息		
	# 消息置为已读结束

	return render(request,'web/shop/10yuan.html',{"iteminfo":iteminfo,"shop_id":shop_id,
		'cart_good_number':cart_good_number})
	
# 红包专区
@sns_userinfo
def redpack_area(request):
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']
	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 	
	# 获取用户
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	shop_id = request.GET['shop_id']
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account
	# 只要
	items = Item.objects.filter(item_type_id=1,merchant__mer_type_id=2,merchant__shop_id=shop_id,item_status_id=1) # 红包专区item
	iteminfo = {}
	for item in items:
		temp_iteminfo = {}
		if item.merchant.mer_type_id == 3:
			temp_iteminfo['surplus'] = item.merchant.price - item.take_part_num
			temp_iteminfo['take_part_price'] = item.take_part_num 
		else:
			temp_iteminfo['surplus'] = item.merchant.price - item.take_part_num
			temp_iteminfo['take_part_price'] = item.take_part_num

		iteminfo[item] = temp_iteminfo
	

	# 查看session购物车的内容
	cart_list = {}
	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']	
	cart_good_number = 0
	# new_cart_list = {} # 过滤后的购物车
	for item_id in cart_list:
		item = Item.objects.get(id=item_id)
		if int(item.merchant.shop_id) != int(shop_id):
			continue
		cart_good_number += cart_list[item_id]	

	# 将session中的message置为已读
	my_have_read_message_list = []
	if 'message_list' in request.session:
		my_have_read_message_list = request.session['message_list']

	for message_id in my_have_read_message_list:
		my_have_read_message = NoticeMsg.objects.get(id=int(message_id))
		my_have_read_message.notice_msg_status_id = 2
		my_have_read_message.save()
	request.session['message_list'] = []	# 置空消息		
	# 消息置为已读结束

	return render(request,'web/shop/redpack_area.html',{"iteminfo":iteminfo,"shop_id":shop_id,
		'cart_good_number':cart_good_number})
	
# 购物车
@sns_userinfo
def cart(request):

	# 信息同步
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']
	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 
	# 获取用户
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		# re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
		# filter_nickname = re_pattern.sub(u'\uFFFD', nickname) 
		# filter_account_name = re_pattern.sub(u'\uFFFD', account_name) 
		# print nickname,account_name,filter_nickname,filter_account_name 	
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account
		account_name = nickname + "的账户"
		print nickname,account_name
		account.name = account_name
		account.save()
	# 获取shop信息
	shop_id = None
	if 'shop_id' in request.GET:
		shop_id = request.GET['shop_id']

	# if shop_id == None:
	# 	if customer.last_login_shop:
	# 		shop_id = customer.last_login_shop.id

	# if customer.last_login_shop == None:
	# 	customer.last_login_shop = Shop.objects.get(id=shop_id)
	# 	customer.save()
	# elif shop_id != customer.last_login_shop.id:
	# 	customer.last_login_shop = Shop.objects.get(id=shop_id)
	# 	customer.save()		
	request.session['shop_id'] = shop_id
	# 获取shop信息结束


	cart_total_number = 0 # 购物车总共的商品数
	if 'cart_total_number' not in request.session:
		cart_total_number = 0
	else:
		cart_total_number = int(request.session['cart_total_number'])

	cart_list = {}
	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']
	# print cart_list

	# 清理购物车，避免跨店
	current_shop_cart_list = {}
	current_shop_total_number = 0
	for item_id in cart_list:
		item = Item.objects.get(id=item_id)
		if int(item.merchant.shop_id) == int(shop_id):
			if item_id in current_shop_cart_list:
				current_shop_cart_list[item_id] += cart_list[item_id]
			else:
				current_shop_cart_list[item_id] = cart_list[item_id]
			current_shop_total_number += cart_list[item_id]
	cart_list = current_shop_cart_list
	cart_total_number = current_shop_total_number

	# 不记录session
	# request.session['cart_list'] = cart_list
	# request.session['cart_total_number'] = current_shop_total_number

	# 重新组织购物车
	total_price = 0
	total_good_number = 0
	item_list = {}
	for item_id in cart_list:
		good_number = cart_list[item_id]
		item = Item.objects.get(id=item_id)
		info = {}
		info['id'] = item_id
		info['number'] = good_number
		if item.merchant.mer_type_id == 3:
			info['price'] = 10 * int(good_number)
		else:
			info['price'] = int(good_number)
		info['surplus'] = item.merchant.price - item.take_part_num
		if info['price'] > info['surplus']:
			info['price'] = info['surplus']
		info['take_part_num'] = item.take_part_num
		item_list[item] = info
		total_price += info['price'] 
		total_good_number += good_number
	# print item_list,'item_list'
	# 将session中的message置为已读
	my_have_read_message_list = []
	if 'message_list' in request.session:
		my_have_read_message_list = request.session['message_list']

	for message_id in my_have_read_message_list:
		my_have_read_message = NoticeMsg.objects.get(id=int(message_id))
		my_have_read_message.notice_msg_status_id = 2
		my_have_read_message.save()
	request.session['message_list'] = []	# 置空消息		
	# 消息置为已读结束

	return render(request,'web/shop/cart.html',{'cart_total_number':cart_total_number,'item_list':item_list
		,"total_price":total_price,"total_good_number":total_good_number,"shop_id":shop_id})

# 添加购物车
@csrf_exempt
def add_cart(request):
	response = {}
	cart_list = {}
	
	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']

	item_id = request.POST['item_id']

	# if item_id in cart_list:
	# 	cart_list[item_id] += 1
	# else:
	# 	cart_list[item_id] = 1

	if item_id not in cart_list:
		cart_list[item_id] = 1

	cart_total_number = 0 # 购物车总共的商品数
	# if 'cart_total_number' in request.session:
	# 	cart_total_number = int(request.session['cart_total_number'])

	for key in cart_list:
		cart_total_number += cart_list[key]

	# 将jsondata预存在session中


	request.session['cart_total_number'] = cart_total_number
	request.session['cart_list'] = cart_list
	response = {'code':0,'msg':'Success','cart_total_number':cart_total_number}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 获取购物车所有数据
@csrf_exempt
def fetch_cart_json_data(request):
	response = {}
	cart_list = {}
	shop_id = None

	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']
	
	if 'shop_id' in request.GET:
		shop_id = int(request.GET['shop_id'])
	elif 'shop_id' in request.POST:
		shop_id = int(request.POST['shop_id'])

	# 清理购物车，避免跨店
	current_shop_cart_list = {}
	current_shop_total_number = 0
	for item_id in cart_list:
		item = Item.objects.get(id=item_id)
		if int(item.merchant.shop_id) == int(shop_id):
			if item_id in current_shop_cart_list:
				current_shop_cart_list[item_id] += cart_list[item_id]
			else:
				current_shop_cart_list[item_id] = cart_list[item_id]
			current_shop_total_number += cart_list[item_id]
	cart_list = current_shop_cart_list
	cart_total_number = current_shop_total_number

	for item_id in cart_list:
		item_num = cart_list[item_id]
		print item_id,item_num
		temp_result = {}
		temp_result["id"] = str(item_id)
		temp_item = Item.objects.get(id=item_id)
		temp_merchant = temp_item.merchant
		if temp_merchant.mer_type.id == 3: # 10元
			temp_result["number"] = str(10 * item_num)
			temp_result["min_buy"] = "10"
		else:
			temp_result["number"] = str( item_num)
			temp_result["min_buy"] = "1"
		temp_result["unit_price"] = "1.0000"		
		# 计算剩余
		temp_total_order_price = 0
		temp_orders = Order.objects.filter(item=temp_item).exclude(order_status_id=3)
		for temp_order in temp_orders:
			if temp_merchant.mer_type.id == 3: # 10元
				temp_total_order_price += 10 * temp_order.order_times
			else:
				temp_total_order_price += temp_order.order_times
		temp_result["residue_count"] = temp_merchant.price - temp_total_order_price
		if temp_result["residue_count"] > 100:
			temp_result["residue_count"] = 100
		response[str(item_id)] = temp_result
	print response
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 修改购物车订单
@csrf_exempt
def change_cart_list(request):
	response = {}

	cart_list = {}
	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']

	cart_good_number = 0
	if 'cart_total_number' not in request.session:
		cart_good_number = 0
	else:
		cart_good_number = int(request.session['cart_total_number'])


	cart_info = {}
	# 获取参数
	item_id = request.POST['id']
	item_event = request.POST['act']
	item_number = 0
	if 'item_number' in request.POST:
		item_number = int(request.POST['item_number'])
	item = Item.objects.get(id=item_id)
	if item.merchant.mer_type.id == 3:
		item_number = item_number / 10
	# print item_id,item_event,item_number,cart_list
	# 根据不同事件进行不同处理 
	if str(item_event) == "minus_cart" or str(item_event) == "plus_cart" or str(item_event) == "buy_number_cart" or str(item_event) == "del_cart":
		if item_id in cart_list:
			item_diff = item_number - cart_list[item_id]
			cart_list[item_id] = item_number
			cart_info["cart_item_num"] = cart_good_number + item_diff
			if item_number == 0:
				del cart_list[item_id]
			request.session['cart_total_number'] = cart_good_number + item_diff
			print cart_info["cart_item_num"]
	# elif str(item_event) == "del_cart":
	request.session['cart_list'] = cart_list
	response['cart_info'] = cart_info
	print response
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 商品详情页
@csrf_exempt
@sns_userinfo
def merchant_detail_info(request):
	# 信息同步
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']
	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 	
	# 获取用户
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account
	print "account name = ",account.name
	print customer.id

	current_url = "http://2.juye51.com" +request.get_full_path()
	request.session['merchant_detail_info_url'] = current_url		

	page_length = 10
	page_id = None
	item_id = None
	total_invest_times = 0
	remain_invest_times = 0
	current_customer_order_times = 0
	# page_id = int(request.POST['page_id'])
	# 获取参数
	if "item_id" in request.POST:
		item_id = int(request.POST['item_id'])
	else:
		item_id = int(request.GET['item_id'])

	# 获取page id
	if "page_id" in request.POST:
		page_id = int(request.POST['page_id'])
	elif 'page_id' in request.GET:
		page_id = int(request.GET['page_id'])
	else:
		page_id = 1 # page id 默认值为1

	# 获取本期所有订单数据
	item = Item.objects.get(id=item_id)
	orders = Order.objects.filter(item=item).exclude(order_status_id=5).exclude(order_status_id=3)
	current_page_orders = orders[(page_id-1)*page_length:page_id*page_length]
	for order in orders:
		if order.item.merchant.mer_type_id == 3:
			total_invest_times += order.order_times * 10
		else:
			total_invest_times += order.order_times
	remain_invest_times = item.merchant.price - item.take_part_num 
	cart_remain_invest_times = remain_invest_times
	# 减去之前记录在购物车的商品数量
	cart_list = {}
	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']	
	new_cart_list = {} # 过滤后的购物车
	for cart_item_id in cart_list:
		if int(cart_item_id) == int(item.id):
			cart_item = Item.objects.get(id=cart_item_id)
			if item.merchant.mer_type_id == 3:
				cart_remain_invest_times -= cart_list[cart_item_id] * 10
			else:
				cart_remain_invest_times -= cart_list[cart_item_id]
	if cart_remain_invest_times > 100: # 最多暂时只能买100发
		cart_remain_invest_times = 100
	# 将session中的message置为已读
	my_have_read_message_list = []
	if 'message_list' in request.session:
		my_have_read_message_list = request.session['message_list']

	for message_id in my_have_read_message_list:
		my_have_read_message = NoticeMsg.objects.get(id=int(message_id))
		my_have_read_message.notice_msg_status_id = 2
		my_have_read_message.save()
	request.session['message_list'] = []	# 置空消息		
	# 消息置为已读结束

	# 获取shop信息
	shop_id = item.merchant.shop_id
	# if customer.last_login_shop == None:
	# 	customer.last_login_shop = Shop.objects.get(id=shop_id)
	# 	customer.save()
	# elif shop_id != customer.last_login_shop.id:
	# 	customer.last_login_shop = Shop.objects.get(id=shop_id)
	# 	customer.save()		
	# 获取shop信息结束

	# 本期中奖号码info数据
	lottery_tickets = []
	for order in orders:
		# 判断中奖用户是否为当前用户
		if order.customer.id == customer.id:
			lottery_tickets += list(LotteryTicket.objects.filter(order=order))
	# lottery_tickets = LotteryTicket.objects

	# 获取当前用户的所有order
	current_customer_orders = Order.objects.filter(customer=customer,item=item,order_status_id=1).order_by('-create_time')
	for current_customer_order in current_customer_orders:
		if current_customer_order.item.merchant.mer_type_id == 3:
			current_customer_order_times += current_customer_order.order_times * 10
		else:
			current_customer_order_times += current_customer_order.order_times		
		# current_customer_order_times += current_customer_order.order_times
	print "current_customer_order_times = ",current_customer_order_times
	# 获取本商品的banner图
	# banner_imgs = item.merchant.banner_img.all()
	banner_imgs = MerchantBannerImg.objects.filter(merchant=item.merchant)
	
	# 查询是否还有剩余数据
	next_page_id = -1
	if len(orders[page_id*page_length:]) > 0:
		next_page_id = page_id + 1 

	# 查看购物车中的物品数
	cart_total_number = 0
	if 'cart_total_number' in request.session:
		cart_total_number = int(request.session['cart_total_number'])

	current_page_orders_info = {}
	for current_page_order in current_page_orders:
		temp_order_info = {}
		if current_page_order.item.merchant.mer_type_id == 3:
			temp_order_info['order_times'] = current_page_order.order_times * 10
		else:
			temp_order_info['order_times'] = current_page_order.order_times
		temp_order_info['create_time_str'] = current_page_order.create_time.strftime('%Y-%m-%d %H:%M:%S')
		current_page_orders_info[current_page_order] = temp_order_info

	current_page_orders_info = sorted(current_page_orders_info.iteritems(), key=lambda d:d[0].create_time, reverse = True)
	# 如果本期已经结束，那么获取中奖用户
	winning_customer = None
	if item.item_status_id == 2 or item.item_status_id == 5 or item.item_status_id == 6:
		winning_customer = LotteryTicket.objects.get(ticket_no=item.winner_code,item=item).order.customer
		# print "/media/" + winning_customer.headimg.name

	proxy_selling = True
	if float(item.merchant.commission_price) == 0.0:
		proxy_selling = False

	return render(request,'web/shop/merchant_detail_info.html',{'orders':current_page_orders_info,'item':item,
		page_id:'page_id','next_page_id':next_page_id,'banner_imgs':banner_imgs,'remain_invest_times':remain_invest_times,
		'current_customer_order_times':current_customer_order_times,'total_invest_times':total_invest_times,
		'cart_total_number':cart_total_number,'lottery_tickets':lottery_tickets,'shop_id':shop_id,"winning_customer":winning_customer,
		"cart_remain_invest_times":cart_remain_invest_times,'proxy_selling':proxy_selling})
###############################################################
#
#             用户模块
# 
###############################################################
# 用户个人页
@sns_userinfo
def selfinfo(request):

	investor_openid = None
	if 'investor_openid' in request.GET:
		investor_openid = request.GET['investor_openid']

	invest_customer = None
	if investor_openid != None:
		invest_customer_tmp_list = Customer.objects.filter(openid=investor_openid)
		if len(invest_customer_tmp_list) != 0:
			invest_customer = invest_customer_tmp_list[0]

	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']

	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']

	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 
	# 查看用户是否存在
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		if invest_customer != None:
			customer.investor_id = invest_customer.id
		customer.save()
	else:
		customer = customers[0]
		account = customer.account

	# 获取shop信息
	shop_id = None
	if 'shop_id' in request.GET:
		shop_id = request.GET['shop_id']

	shop = Shop.objects.get(id=int(shop_id))
	# 将商店和用户关联起来
	if len(customer.shops.filter(id=int(shop_id))) == 0:
		print shop_id,customer.id,"还未关联"
		customer.shops.add(shop)
		customer.save()

	# 查看session购物车的内容
	cart_list = {}
	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']	
	cart_good_number = 0
	# new_cart_list = {} # 过滤后的购物车
	for item_id in cart_list:
		item = Item.objects.get(id=item_id)
		if int(item.merchant.shop_id) != int(shop_id):
			continue
		cart_good_number += cart_list[item_id]

	# 将session中的message置为已读
	my_have_read_message_list = []
	if 'message_list' in request.session:
		my_have_read_message_list = request.session['message_list']

	for message_id in my_have_read_message_list:
		my_have_read_message = NoticeMsg.objects.get(id=int(message_id))
		my_have_read_message.notice_msg_status_id = 2
		my_have_read_message.save()
	request.session['message_list'] = []	# 置空消息		
	# 消息置为已读结束

	my_messages = NoticeMsg.objects.filter(customer=customer,notice_msg_status_id=1,shop=shop) | NoticeMsg.objects.filter(customer=customer,notice_msg_status_id=1,shop=None)
	# request.session['message_list'] = my_messages
	my_messages_length = len(my_messages)
	return render(request,'web/user/self.html',{"cart_good_number":cart_good_number,"customer":customer,
		"account":account,"shop_id":shop_id,"my_messages_length":my_messages_length})

# 客服页面
def self_customer(request):
	investor_openid = None
	if 'investor_openid' in request.GET:
		investor_openid = request.GET['investor_openid']

	invest_customer = None
	if investor_openid != None:
		invest_customer_tmp_list = Customer.objects.filter(openid=investor_openid)
		if len(invest_customer_tmp_list) != 0:
			invest_customer = invest_customer_tmp_list[0]

	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']

	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']

	# 查看用户是否存在
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		if invest_customer != None:
			customer.investor_id = invest_customer.id
		customer.save()
	else:
		customer = customers[0]
		account = customer.account

	# 获取shop信息
	shop_id = None
	if 'shop_id' in request.GET:
		shop_id = request.GET['shop_id']

	# if shop_id == None:
	# 	if customer.last_login_shop:
	# 		shop_id = customer.last_login_shop.id

	# if customer.last_login_shop == None:
	# 	customer.last_login_shop = Shop.objects.get(id=shop_id)
	# 	customer.save()
	# elif shop_id != customer.last_login_shop.id:
	# 	customer.last_login_shop = Shop.objects.get(id=shop_id)
	# 	customer.save()		
	shop = Shop.objects.get(id=shop_id)
	# 获取shop信息结束

	# 查看session购物车的内容
	cart_list = {}
	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']	
	cart_good_number = 0
	# new_cart_list = {} # 过滤后的购物车
	for item_id in cart_list:
		item = Item.objects.get(id=item_id)
		if int(item.merchant.shop_id) != int(shop_id):
			continue
		cart_good_number += cart_list[item_id]

	# 将session中的message置为已读
	my_have_read_message_list = []
	if 'message_list' in request.session:
		my_have_read_message_list = request.session['message_list']

	for message_id in my_have_read_message_list:
		my_have_read_message = NoticeMsg.objects.get(id=int(message_id))
		my_have_read_message.notice_msg_status_id = 2
		my_have_read_message.save()
	request.session['message_list'] = []	# 置空消息		
	# 消息置为已读结束

	return render(request,'web/user/self_customer_service.html',{"cart_good_number":cart_good_number,"customer":customer,
		"account":account,"shop_id":shop_id,"shop":shop })		
####################################################################
#
# 	代卖
#
#####################################################################

# 发起代卖请求
@csrf_exempt
@sns_userinfo
def submit_proxy_selling_request(request):
	response = {}
	merchant_id = int(request.GET['merchant_id'])
	merchant = Merchant.objects.get(id=merchant_id)
	# init_proxy_selling_tag = 1 # 初次代卖标记
	# 信息同步
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']
	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 	
	# 获取用户
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account

	# 查看是否有代卖记录
	items = Item.objects.filter(proxy_sale_customer=customer,merchant=merchant,
		item_status_id=1,item_type_id=2)
	if len(items) == 0: # 不存在代卖记录
		response['status'] = 0
		# # 新建代卖消息
		# msg_title = "代卖成功"
		# msg_context = "代卖商品\"%s\"成功，期号为%s，代卖本期成功后可获得高达%.1f的佣金，祝您发财~" % (items[0].merchant.name,items[0].item_code,item.merchant.commission_price)
		# new_msg = NoticeMsg.objects.create(shop_id=shop_id,customer=customer,title=msg_title,notice_msg_status_id=1,context=msg_context)	
		# new_msg.save()			
		# # 新建消息结束		
	else:
		response['status'] = 1 # 存在代卖记录
		response['proxy_item_id'] = str(items[0].id)
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))


# 代卖商品列表页
@sns_userinfo
def my_selling_list(request):
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']
	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 	
	# 获取用户
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	shop_id = request.GET['shop_id']
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account
	items = Item.objects.filter(proxy_sale_customer=customer,item_type_id=2,merchant__shop_id=shop_id) # 任何状态都显示
	iteminfo = {}
	for item in items:
		temp_iteminfo = {}
		if item.merchant.mer_type_id == 3:
			temp_iteminfo['surplus'] = item.merchant.price - item.take_part_num
			temp_iteminfo['take_part_price'] = item.take_part_num 
		else:
			temp_iteminfo['surplus'] = item.merchant.price - item.take_part_num
			temp_iteminfo['take_part_price'] = item.take_part_num

		iteminfo[item] = temp_iteminfo
	

	# 查看session购物车的内容
	cart_list = {}
	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']	
	cart_good_number = 0
	# new_cart_list = {} # 过滤后的购物车
	for item_id in cart_list:
		item = Item.objects.get(id=item_id)
		if int(item.merchant.shop_id) != int(shop_id):
			continue
		cart_good_number += cart_list[item_id]

	# 将session中的message置为已读
	my_have_read_message_list = []
	if 'message_list' in request.session:
		my_have_read_message_list = request.session['message_list']

	for message_id in my_have_read_message_list:
		my_have_read_message = NoticeMsg.objects.get(id=int(message_id))
		my_have_read_message.notice_msg_status_id = 2
		my_have_read_message.save()
	request.session['message_list'] = []	# 置空消息		
	# 消息置为已读结束

	# 获取代卖列表
	return render(request,'web/user/my_selling_list.html',{"iteminfo":iteminfo,"shop_id":shop_id,
		'cart_good_number':cart_good_number})
	
# 首次代卖商品请求
@sns_userinfo
def selling_merchant_request(request):
	merchant_id = int(request.GET['merchant_id'])
	merchant = Merchant.objects.get(id=merchant_id)
	# init_proxy_selling_tag = 1 # 初次代卖标记
	# 信息同步
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']
	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 	
	# 获取用户
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account

	# 新建Item
	item = None
	items = Item.objects.filter(merchant=merchant,item_status_id=1,item_type_id=2,proxy_sale_customer=customer) 
	if len(items) == 0:
		item = Item.objects.create(merchant=merchant,item_status_id=1,item_type_id=2,proxy_sale_customer=customer)
		item.item_code = str(100000000 + int(item.id))
		item.save()		
	else:
		item = items[0]

	# 获取商品的banner图
	banner_imgs = MerchantBannerImg.objects.filter(merchant=item.merchant)
	# 新建代卖消息
	# msg_title = "代卖成功"
	# msg_context = "代卖商品\"%s\"成功，期号为%s，代卖本期成功后可获得高达%.1f的佣金，祝您发财~" % (item.merchant.name,item.item_code,item.merchant.commission_price)
	# new_msg = NoticeMsg.objects.create(shop_id=shop_id,customer=customer,title=msg_title,notice_msg_status_id=1,context=msg_context)	
	# new_msg.save()			
	# 新建消息结束

	return render(request,'web/user/selling_merchant.html',{'item':item,'banner_imgs':banner_imgs})


# 代卖详情页
@sns_userinfo
def selling_merchant_detail_info(request):
	duobao_user_logger = logging.getLogger('user')
	current_url = "http://2.juye51.com" +request.get_full_path()
	request.session['proxy_selling_url'] = current_url		
	merchant_id = int(request.GET['merchant_id'])
	merchant = Merchant.objects.get(id=merchant_id)
	# init_proxy_selling_tag = 1 # 初次代卖标记
	# 信息同步
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']
	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 	
	# 获取用户
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account



	# 新建Item
	item = None
	items = Item.objects.filter(merchant=merchant,item_status_id=1,item_type_id=2,proxy_sale_customer=customer) 
	if len(items) == 0:
		item = Item.objects.create(merchant=merchant,item_status_id=1,item_type_id=2,proxy_sale_customer=customer)
		item.item_code = str(100000000 + int(item.id))	
		item.save()		
	else:
		item = items[0]
	item_id = item.id

	# 生成短连接
	short_url_req = "http://api.t.sina.com.cn/short_url/shorten.json?source=3271760578&url_long=%s/shop/merchant_detail_info/?item_id=%d" %(WxPayConf_pub.WEB_DOMAIN,item_id)
	request_result = urllib.urlopen(short_url_req).read()
	proxy_selling_short_url = json.loads(request_result)[0]['url_short']
	item.proxy_sale_qr_code = proxy_selling_short_url
	item.save()

	# 生成短连接对应的二维码
	qr_code_url = "http://pan.baidu.com/share/qrcode?w=280&h=280&url=%s" % proxy_selling_short_url



	# 新建代卖消息
	msg_title = "代卖成功"
	msg_context = "代卖商品\"%s\"成功，期号为%s，代卖本期成功后可获得高达%.1f的佣金，使用微信分享、商品二维码即可分享。" % (item.merchant.name,item.item_code,item.merchant.commission_price)
	new_msg = NoticeMsg.objects.create(shop=merchant.shop,customer=customer,title=msg_title,notice_msg_status_id=1,context=msg_context)	
	new_msg.save()			
	# 新建消息结束

	# 微信提醒代卖消息
	item_link = "http://2.juye51.com/shop/merchant_detail_info/?page_id=1&item_id=%d" % int(item_id)
	client = fetch_wechatpy_client()
	try:
		client.message.send_text(customer.openid,"%s: \n 恭喜您代卖<a href='%s'>商品\"%s\"</a>成功，期号为%s。\n完成本期后可获得高达%.1f的佣金，使用微信分享、商品二维码即可分享。" % (customer.name,item_link,item.merchant.name,item.item_code,item.merchant.commission_price))				            		
	except:
		duobao_user_logger.info("代卖请求发送消息失败")
	# client.message.send_text(customer.openid,"<img src='%s'>" % item.proxy_sale_qr_code)
	# 微信提醒代卖消息结束




	pyq_title = "%s代卖店里的%s,欢迎来一元夺宝" % (customer.name,item.merchant.name)
	hy_desc = "%s代卖店里的%s,欢迎来一元夺宝" % (customer.name,item.merchant.name)
	hy_title = "%s的一元夺宝代卖" % customer.name
	img_url = "http://2.juye51.com/media/%s" % item.merchant.mer_img.name
	# print proxy_selling_short_url
	return render(request,'web/merchant/proxy_selling_info_page.html',{'item_id':item.id,'item':item,
		'proxy_selling_short_url':proxy_selling_short_url,'qr_code_url':qr_code_url,
		'pyq_title':pyq_title,'hy_desc':hy_desc,'hy_title':hy_title,'img_url':img_url})
##################################################################3
#
# 代卖结束
#
####################################################################

# 用户充值页面
def pay_coins(request):
	shop_id = request.GET['shop_id']
	return render(request,'web/user/pay_coins.html',{'shop_id':shop_id})

# 后门~
@sns_userinfo
def wechat_pay_success(request):

	openid = request.session['openid']
	money = request.GET['money']

	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		userinfo = request.session['userinfo']
		headimg = userinfo['headimgurl']
		nickname = userinfo['nickname']		
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account	
	account.balance_coins += int(money)
	account.save()
	print "money = ", money
	return HttpResponseRedirect('/user/selfinfo/')


def pay_success_jumper(request):
	print "pay_success_jumper enter"
	# shop_id = 1
	shop_id = request.session['shop_id']
	print "shop_id = ",shop_id
	return render(request,'web/user/pay_success_jumper.html',{'shop_id':shop_id})

# 充值成功跳转 
def recharge_success_jumper(request):
	shop_id = request.GET['shop_id']
	return render(request,'web/user/recharge_success_jumper_page.html',
		{'shop_id':shop_id})

# 微信支付等待结果中间页面
def order_wait_wechat_pay_result(request):
	shop_id = request.GET['shop_id']
	return render(request,'web/user/order_wait_wechat_pay_result.html',{'shop_id':shop_id})

# 微信支付结果跳转页面（根据队列等判断调用成功页面、还是失败页面）
@sns_userinfo
def order_wechat_pay_result_jumper(request):
	duobao_record_logger = logging.getLogger('record')
	# 信息同步
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']
	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 	
	# 获取用户
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account

	shop_id = request.session['shop_id']
	# todo: 此处应该有队列
	# 获取transaction
	transaction_id = int(request.session['need_to_pay_transaction_id'])
	transaction = Transaction.objects.get(id=transaction_id)
	print "transaction.transaction_status_id = ",transaction.transaction_status_id 
	if transaction.transaction_status_id == 2: # 交易状态代表交易成功
		# 清除购物车list
		# cart_list = request.session['cart_list']
		# print "cart_list,",cart_list

		# orders = transaction.orders.all()
		# for order in orders:
		# 	item = order.item
		# 	good_number = cart_list[str(item.id)]
		# 	if item.merchant.mer_type_id == 3:
		# 		item.take_part_num += 10 * good_number
		# 	else:
		# 		item.take_part_num += good_number

		# 	merchant_price = item.merchant.price

		# 	# 分配奖券
		# 	ticket_number = good_number
		# 	if item.merchant.mer_type_id == 3:
		# 		ticket_number = good_number * 10		

		# 	duobao_record_logger.info("[结算分配奖券-微信支付] 对用户%s, 用户ID为%d ITEM_ID为%d 即将分配%d个奖券" % (nickname,customer.id,item.id,ticket_number))		
		# 	# 查询已经分配的奖券
		# 	item_tickets = LotteryTicket.objects.filter(item=item)
		# 	item_ticket_numbers = []
		# 	for item_ticket in item_tickets:
		# 		item_ticket_numbers.append(item_ticket.ticket_no)
		# 	duobao_record_logger.info("[结算分配奖券-微信支付] 期号为%s的项目,已经参与了%d次,已经分配奖券%d张" % (item.item_code,item.take_part_num,len(item_tickets)))

		# 	for i in range(0,ticket_number):
		# 		random_ticket_no = random.randint(0,merchant_price-1)
		# 		# 直到找到未分配的奖券
		# 		while True:
		# 			tickets = LotteryTicket.objects.filter(item=item,ticket_no=random_ticket_no + 100000000)
		# 			if len(tickets) == 0:
		# 				new_ticket = LotteryTicket.objects.create(item=item,ticket_no=random_ticket_no + 100000000,order=order)
		# 				duobao_record_logger.info("[结算分配奖券-微信支付] 用户ID: %d 期号为%s的项目,成功分配第%d张奖券,号码为%s" % (customer.id,item.item_code,i+1,new_ticket.ticket_no))
		# 				break
		# 			else:
		# 				random_ticket_no = (random_ticket_no + 1) % merchant_price
				

		# 	# 如果本期商品结束，则修改状态（等待开奖）
		# 	if item.merchant.price == item.take_part_num:
		# 		item.item_status_id = 4
		# 		# 建立新的一期
		# 		if item.merchant.auto_up_shelve == True and item.item_type.id == 1: 
		# 			new_item = Item.objects.create(merchant=item.merchant,item_status_id=1,item_type_id=1)
		# 			new_item.item_code = str(100000000 + int(new_item.id))
		# 			new_item.save()						
		# 	item.save()

		request.session['cart_total_number'] = 0
		request.session['cart_list'] = {}
		del request.session['cart_total_number']
		del request.session['cart_list']		
	if 'need_to_pay_transaction_id' in request.session:	
		del request.session['need_to_pay_transaction_id']
	# todo 目前之后成功逻辑
	return render(request,'web/user/order_wechat_pay_result_jumper.html',{"shop_id":shop_id})



########################################################
#
#  支付与购物车
#
#########################################################



# 提交购物车中商品
@csrf_exempt
def submit_cart_merchant(request):
	
	shop_id = None
	if 'shop_id' in request.GET:
		shop_id = int(request.GET['shop_id'])
	elif 'shop_id' in request.POST:
		shop_id = int(request.POST['shop_id'])	
	response = {"jump":"/user/submit_order_page/?shop_id=%d" % int(shop_id) ,"status":1}
	# 获取购物车信息
	cart_list = {}
	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']
	# 清理购物车，避免跨店
	current_shop_cart_list = {}
	current_shop_total_number = 0
	for item_id in cart_list:
		item = Item.objects.get(id=item_id)
		if int(item.merchant.shop_id) == int(shop_id):
			if item_id in current_shop_cart_list:
				current_shop_cart_list[item_id] += cart_list[item_id]
			else:
				current_shop_cart_list[item_id] = cart_list[item_id]
			current_shop_total_number += cart_list[item_id]
	cart_list = current_shop_cart_list
	cart_total_number = current_shop_total_number

	total_price = 0
	# if 'total_price' in request.session:
	# 	total_price = request.session['total_price']
	# else:
	for item_id in cart_list:
		item_id_digit = int(item_id)
		good_number = int(cart_list[item_id])
		temp_merchant = Item.objects.get(id=item_id_digit).merchant
		if temp_merchant.mer_type_id == 3:
			total_price += 10 * good_number
		else:
			total_price += good_number
	# 如果购物车为空，则不跳转
	if total_price == 0:
		response = {'status': 0, 'info': "您的购物车为空！"}
	request.session['total_price'] = total_price	
	# response = {"into":"#","status":1}
	print "cart submit params = ",response
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 提交订单
@sns_userinfo
# @csrf_exempt
def submit_order_page(request):
	# 信息同步
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']	
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']
	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 	
	# 查看用户是否存在
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account	
	shop_id = request.GET['shop_id']
	# 获得余额
	balance = account.balance_coins
	# 获取购物车信息
	cart_list = {}
	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']
	print cart_list,'cart_list'

	total_price = 0
	if 'total_price' in request.session:
		total_price = request.session['total_price']
	else:
		for item_id in cart_list:
			item_id_digit = int(item_id)
			good_number = int(cart_list[item_id])
			temp_merchant = Item.objects.get(id=item_id_digit).merchant
			if temp_merchant.mer_type_id == 3:
				total_price += 10 * good_number
			else:
				total_price += good_number
		request.session['total_price'] = total_price
	print 'total_price',total_price

	# 将session中的message置为已读
	my_have_read_message_list = []
	if 'message_list' in request.session:
		my_have_read_message_list = request.session['message_list']

	for message_id in my_have_read_message_list:
		my_have_read_message = NoticeMsg.objects.get(id=int(message_id))
		my_have_read_message.notice_msg_status_id = 2
		my_have_read_message.save()
	request.session['message_list'] = []	# 置空消息		
	# 消息置为已读结束
	# return HttpResponseRedirect('/user/selfinfo/')
	return render(request,'web/user/submit_order_page.html',{'total_price':total_price,
		"balance":balance,'shop_id':shop_id})

# 更新支付方式
@csrf_exempt
def choose_submit_order_type(request):

	total_price = int(request.session['total_price'])
	payment = None
	if 'payment' not in request.POST:
		payment = 0 
	else:
		payment = int(request.POST['payment'])
	response = {}
	if payment == 3:
		response['html'] = """<html>
			 <head></head>
			 <body>
			  <div class="item-common list-li"> 
			   <span class="item-label fl">商品总价</span> 
			   <div class="item-content red fr">
			    %d元
			   </div> 
			   <div class="clear"></div> 
			  </div> 
			  <div class="item-common list-li"> 
			   <span class="item-label fl">支付方式</span> 
			   <div class="item-content red fr">
			    微信支付
			   </div> 
			   <div class="clear"></div> 
			  </div> 
			  <div class="item-common list-li"> 
			   <span class="item-label fl">总计</span> 
			   <div class="item-content red fr">
			    %d元
			   </div> 
			   <div class="clear"></div> 
			  </div> 
			  <div class="item-common list-li" style="border-bottom:none;"> 
			   <span class="item-label fl">应付总额</span> 
			   <div class="item-content red fr">
			   	%d元
			   </div> 
			   <div class="clear"></div> 
			  </div> 
			 </body>
			</html>""" % (total_price,total_price,total_price)
	elif payment == 0:
		response['html'] = """<html>
			 <head></head>
			 <body>
			  <div class="item-common list-li"> 
			   <span class="item-label fl">商品总价</span> 
			   <div class="item-content red fr">
			    %d元
			   </div> 
			   <div class="clear"></div> 
			  </div> 
			  <div class="item-common list-li"> 
			   <span class="item-label fl">总计</span> 
			   <div class="item-content red fr">
			    %d元
			   </div> 
			   <div class="clear"></div> 
			  </div> 
			  <div class="item-common list-li" style="border-bottom:none;"> 
			   <span class="item-label fl">应付总额</span> 
			   <div class="item-content red fr">
			   	%d元
			   </div> 
			   <div class="clear"></div> 
			  </div> 
			 </body>
			</html>""" % (total_price,total_price,total_price)
	elif payment == 1:
		response['html'] = """<html>
			 <head></head>
			 <body>
			  <div class="item-common list-li"> 
			   <span class="item-label fl">商品总价</span> 
			   <div class="item-content red fr">
			    %d元
			   </div> 
			   <div class="clear"></div> 
			  </div> 
			  <div class="item-common list-li"> 
			   <span class="item-label fl">支付方式</span> 
			   <div class="item-content red fr">
			    夺宝币余额支付
			   </div> 
			   <div class="clear"></div> 
			  </div> 
			  <div class="item-common list-li"> 
			   <span class="item-label fl">总计</span> 
			   <div class="item-content red fr">
			    %d元
			   </div> 
			   <div class="clear"></div> 
			  </div> 
			  <div class="item-common list-li" style="border-bottom:none;"> 
			   <span class="item-label fl">应付总额</span> 
			   <div class="item-content red fr">
			   	%d元
			   </div> 
			   <div class="clear"></div> 
			  </div> 
			 </body>
			</html>""" % (total_price,total_price,total_price)			
	response['is_pick'] = None
	response['pay_price'] = 1
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))


# 用户提交支付返回结果
@csrf_exempt
@sns_userinfo
def submit_order_result(request):
	response = {}
	shop_id = request.GET['shop_id']
	openid = request.session['openid']
	userinfo = request.session['userinfo']	
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']
	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 	
	# 查看用户是否存在
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account	
	duobao_logger = logging.getLogger('record')
	print "submit_order_result :" , customer.name
	duobao_logger.info("用户 %s 进入结算页面,用户ID为%d" % (nickname,customer.id))
	cart_list = {}
	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']

	payment = 0
	balance = account.balance_coins
	total_price = int(request.session['total_price'])

	# 将所有待支付的交易变成失效订单
	need_to_pay_transactions = Transaction.objects.filter(customer=customer,transaction_status_id=1)
	for need_to_pay_transaction in need_to_pay_transactions:
		need_to_pay_transaction.transaction_status_id = 3
		need_to_pay_transaction.save()

	# 清空待支付session中交易id 
	if 'need_to_pay_transaction_id' in request.session:
		del request.session['need_to_pay_transaction_id']

	# 判断购物车中记载的商品 是否被其他人抢走
	for cart_item_id in cart_list:
		cart_item_id_digit = int(cart_item_id)
		cart_good_number = int(cart_list[cart_item_id])
		cart_temp_item = Item.objects.select_for_update().get(id=cart_item_id_digit) # 锁表
		cart_good_price = 0
		if cart_temp_item.merchant.mer_type_id == 3:
			cart_good_price = 10 * cart_good_number
		else:
			cart_good_price = cart_good_number		
		# 判断购物车内商品是否足够
		if cart_temp_item.merchant.price - cart_temp_item.take_part_num < cart_good_price:
			notice_info = "您选购的%s期号%s已不足%d人次，请调整购物车重新购买" % (cart_temp_item.merchant.name,cart_temp_item.item_code,cart_good_price)
			response = {'status': 0, 'info': notice_info}
			return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	if 'payment' not in request.POST:
		payment = 0
	else:
		payment = int(request.POST['payment'])
	if payment == 0:
		response = {'status': 0, 'info': "请选择支付方式"}
	elif payment == 1: # 夺宝币余额支付
		duobao_logger.info("[结算] 用户使用夺宝币结算!");
		if balance < total_price:
			response = {'status': 0, 'info': "账户夺宝币余额不足，请在个人中心充值"}
		else:
			# 建立新交易对象
			
			transaction = Transaction.objects.create(customer=customer,transaction_status_id=2) # 成功完结
			transaction_no = None
			try:
				transaction_no = datetime.datetime.now().strftime("%Y%m%d") + "10000000" + str(transaction.id)
			except:
				transaction_no = datetime.now().strftime("%Y%m%d") + "10000000" + str(transaction.id)
			transaction.transaction_no = transaction_no
			transaction.save()
			duobao_logger.info("[结算] 建立新Transaction, ID为%d,transaction_no为%s!" % (transaction.id,transaction.transaction_no));
			# 建立order

			for item_id in cart_list:
				item_id_digit = int(item_id)
				good_number = int(cart_list[item_id])
				temp_item = Item.objects.get(id=item_id_digit)
				new_order = Order.objects.create(order_status_id=1,customer=customer,item=temp_item,order_times=good_number)

				# 分配奖券数量
				ticket_number = good_number
				if temp_item.merchant.mer_type_id == 3:
					ticket_number = good_number * 10
				print ticket_number	
				duobao_logger.info("[结算分配奖券] 对用户%s, 用户ID为%d ITEM_ID为%d 即将分配%d个奖券" % (nickname,customer.id,item_id_digit,ticket_number))
				# 查询已经分配的奖券
				item_tickets = LotteryTicket.objects.filter(item=temp_item)
				item_ticket_numbers = []
				for item_ticket in item_tickets:
					item_ticket_numbers.append(item_ticket.ticket_no)
				duobao_logger.info("[结算分配奖券] 期号为%s的项目,已经参与了%d次,已经分配奖券%d张" % (temp_item.item_code,temp_item.take_part_num,len(item_tickets)))
				
				temp_take_part_price = 0
				if temp_item.merchant.mer_type_id == 3:
					temp_item.take_part_num += 10 * good_number
					temp_take_part_price = 10 * good_number
				else:
					temp_item.take_part_num += good_number	
					temp_take_part_price = good_number

				merchant_price = temp_item.merchant.price # 项目对应商品价格
				duobao_logger.info("[结算] 建立order: ITEM_ID: %d , 购买人次: %d , order id: %d" % (item_id_digit,temp_take_part_price,new_order.id))

				for i in range(0,ticket_number):
					random_ticket_no = random.randint(0,merchant_price-1)
					# 直到找到未分配的奖券
					while True:
						tickets = LotteryTicket.objects.filter(item=temp_item,ticket_no=random_ticket_no + 100000000)
						if len(tickets) == 0:
							new_ticket = LotteryTicket.objects.create(item=temp_item,ticket_no=random_ticket_no + 100000000,order=new_order)
							duobao_logger.info("[结算分配奖券] 用户ID: %d 期号为%s的项目,成功分配第%d张奖券,号码为%s" % (customer.id,temp_item.item_code,i+1,new_ticket.ticket_no))
							break
						else:
							random_ticket_no = (random_ticket_no + 1) % merchant_price
				# 	print i,random_ticket_no
				
				duobao_logger.info("[结算分配奖券] 分配结束奖券")
				duobao_logger.info("[结算分配奖券] 对用户%s, 用户ID为%d ITEM_ID为%d 分配%d个奖券" % (nickname,customer.id,item_id_digit,ticket_number))
				# 新建消息
				# msg_title = "参与夺宝成功"
				# msg_context = "您成功参与\"%s的第%s期活动\"%d人次，并已经分配中奖号码。具体详情请进入夺宝记录查看~祝您获奖" % (temp_item.merchant.name,temp_item.item_code,temp_take_part_price)
				# new_msg = NoticeMsg.objects.create(shop_id=shop_id,customer=customer,title=msg_title,notice_msg_status_id=1,context=msg_context)	
				# new_msg.save()			
				# 新建消息结束
				item_link = "http://2.juye51.com/shop/merchant_detail_info/?page_id=1&item_id=%d" % item_id_digit 
				record_link = "http://2.juye51.com/record/my_all_records/?shop_id=%d" % int(shop_id)
				client = fetch_wechatpy_client()
				try:
					client.message.send_text(customer.openid,"%s: \n您成功参与<a href='%s'>%s的第%s期活动</a>%d人次，并已经分配中奖号码。\n具体详情请<a href='%s'>进入夺宝记录</a>查看~祝您获奖" % (customer.name,item_link,temp_item.merchant.name,temp_item.item_code,temp_take_part_price,record_link))				
				except:
					print "微信发送消息失败！"

				# 如果本期商品结束，则修改状态
				if temp_item.merchant.price == temp_item.take_part_num:
					temp_item.item_status_id = 4
					# 建立新的一期
					if temp_item.merchant.auto_up_shelve == True and temp_item.item_type.id == 1: 
						new_item = Item.objects.create(merchant=temp_item.merchant,item_status_id=1,item_type_id=1)
						new_item.item_code = str(100000000 + int(new_item.id))
						new_item.save()		
						duobao_logger.info("[结算] 期号为%s自动上架" % new_item.item_code)		
				temp_item.save()
				transaction.orders.add(new_order)
			# 清空购物车
			del request.session['cart_total_number']
			del request.session['cart_list']
			# 扣款
			account.balance_coins -= total_price
			account.save()

			del request.session['total_price']
			response = {'status': 1 , 'info': "success",'jump':'/user/pay_success_jumper/'}

	elif payment == 3: # 微信支付
		duobao_logger.info("[结算] 用户使用微信支付结算!");
		request.session['total_price'] = total_price
		# 建立新交易对象
		transaction = Transaction.objects.create(customer=customer,transaction_status_id=1) # 待支付的交易对象
		transaction_no = None
		# TODO彻查

		try:
			transaction_no = datetime.datetime.now().strftime("%Y%m%d") + "10000000" + str(transaction.id)
		except:
			transaction_no = datetime.now().strftime("%Y%m%d") + "10000000" + str(transaction.id)
		transaction.transaction_no = transaction_no
		transaction.save()
		duobao_logger.info("[结算] 建立新的transaction %d " % transaction.id);
		request.session['need_to_pay_transaction_id'] = transaction.id
		# 建立order
		for item_id in cart_list:
			item_id_digit = int(item_id)
			good_number = int(cart_list[item_id])
			temp_item = Item.objects.get(id=item_id_digit)
			new_order = Order.objects.create(order_status_id=5,customer=customer,item=temp_item,order_times=good_number)
			duobao_logger.info("[结算] 建立新的order, order id为 %d " % new_order.id);
			transaction.orders.add(new_order)	
		# 此处不清空购物车，待回调成功
		response = {'status': 1 , 'info': "success",
		'jump':'/user/order_wechat_payment_submit/?shop_id=%d&need_to_pay_transaction_id=%d&total_price=%d' % (int(shop_id),int(transaction.id),int(total_price))}
		# return HttpResponseRedirect('http://www.baidu.com')
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 订单中选择微信支付方法
def order_wechat_payment_submit(request):
	total_price = request.session['total_price']
	shop_id = request.GET['shop_id']
	need_to_pay_transaction_id = int(request.GET['need_to_pay_transaction_id'])
	return render(request,'web/user/order_wechat_pay.html',{'total_price':total_price,'shop_id':shop_id,'need_to_pay_transaction_id':need_to_pay_transaction_id})

# 充值提交微信支付请求
@csrf_exempt
@catch
@sns_userinfo
def submit_pay_request(request):
	"""获取支付信息"""
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid

	openid = request.session['openid']
	money = int(request.POST['money']) * 100 # 单位是元
	# print money
	jsApi = JsApi_pub()
	time_unify_start = time.time()	
	unifiedOrder = UnifiedOrder_pub()
	unifiedOrder.setParameter("openid",openid) #商品描述
	unifiedOrder.setParameter("body","红包接龙活动") #商品描述
	timeStamp = time.time()
	# print 'unifiedOrder time delta ', timeStamp - time_unify_start
	out_trade_no = "{0}{1}".format(WxPayConf_pub.APPID, int(timeStamp*100))
	unifiedOrder.setParameter("out_trade_no", out_trade_no) #商户订单号
	unifiedOrder.setParameter("total_fee", str(money)) #总金额
	unifiedOrder.setParameter("notify_url", WxPayConf_pub.RECHARGE_NOTIFY_URL) #通知地址 
	unifiedOrder.setParameter("trade_type", "JSAPI") #交易类型
	unifiedOrder.setParameter("attach", "juye_tech") #附件数据，可分辨不同商家(string(127))	
	# unifiedOrder.setParameter("shop_id",str(shop_id))
	time_unify_end = time.time()
	try:
		prepay_id = unifiedOrder.getPrepayId()
		jsApi.setPrepayId(prepay_id)
		jsApiParameters = jsApi.getParameters()
		# print prepay_id,'prepay_id'
		# print 'pay detail end function delta!!!', time_unify_end - time_paydetail_start
	except Exception as e:
		print(e)
	else:
		print jsApiParameters,' 打印微信支付参数'
		return HttpResponse(jsApiParameters)



# 订单中提交微信支付订单
@sns_userinfo
@catch
@csrf_exempt
def submit_wechat_order_pay(request):
	"""获取支付信息"""
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid

	openid = request.session['openid']
	money = int(request.POST['money']) * 100 # 单位是元
	# print money
	jsApi = JsApi_pub()
	time_unify_start = time.time()	
	unifiedOrder = UnifiedOrder_pub()
	unifiedOrder.setParameter("openid",openid) #商品描述
	unifiedOrder.setParameter("body","桔叶科技一元夺宝") #商品描述
	timeStamp = time.time()
	# print 'unifiedOrder time delta ', timeStamp - time_unify_start
	out_trade_no = "{0}{1}".format(WxPayConf_pub.APPID, int(timeStamp*100))
	unifiedOrder.setParameter("out_trade_no", out_trade_no) #商户订单号
	unifiedOrder.setParameter("total_fee", str(money)) #总金额
	unifiedOrder.setParameter("notify_url", WxPayConf_pub.ORDER_WECHAT_PAY_NOTIFY_URL) #通知地址 
	unifiedOrder.setParameter("trade_type", "JSAPI") #交易类型
	unifiedOrder.setParameter("attach",str(request.session['need_to_pay_transaction_id'])) #附件数据，可分辨不同商家(string(127))	

	time_unify_end = time.time()
	try:
		prepay_id = unifiedOrder.getPrepayId()
		jsApi.setPrepayId(prepay_id)
		jsApiParameters = jsApi.getParameters()
		# print prepay_id,'prepay_id'
		# print 'pay detail end function delta!!!', time_unify_end - time_paydetail_start
	except Exception as e:
		print(e)
	else:
		# print jsApiParameters
		return HttpResponse(jsApiParameters)

	# return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))


###############################################################
#
#             支付回调
# 
###############################################################

# 充值回调
@csrf_exempt
@catch
def wechat_recharge_payback(request):
    """支付回调"""
    xml = request.body
 
    #使用通用通知接口
    notify = Notify_pub()
    notify.saveData(xml)
    #验证签名，并回应微信。
    #对后台通知交互时，如果微信收到商户的应答不是成功或超时，微信认为通知失败，
    #微信会通过一定的策略（如30分钟共8次）定期重新发起通知，
    #尽可能提高通知的成功率，但微信不保证通知最终能成功
    if not notify.checkSign():
        print 'sign check failed!'
        notify.setReturnParameter("return_code", FAIL) #返回状态码
        notify.setReturnParameter("return_msg", "签名失败") #返回信息
    else:
        result = notify.getData()
        print 'pay back result', result
        if result["return_code"] == FAIL:
            notify.setReturnParameter("return_code", FAIL)
            notify.setReturnParameter("return_msg", "通信错误")
            print '通信错误'
        elif result["result_code"] == FAIL:
            notify.setReturnParameter("return_code", FAIL)
            notify.setReturnParameter("return_msg", result["err_code_des"])
            print 'result code 错误'
        else:
            notify.setReturnParameter("return_code", SUCCESS)
            out_trade_no = result["out_trade_no"] #商户系统的订单号，与请求一致。	
            openid = result["openid"]
            recharge_fee = int(result["total_fee"]) / 100
            customer = Customer.objects.get(openid=openid)
            account = customer.account
            account.balance_coins += recharge_fee
            account.save() # 充值
            # 新建消息
            msg_context = "您已经成功充值%d夺宝币" % recharge_fee
            new_msg = NoticeMsg.objects.create(customer=customer,title="充值成功",notice_msg_status_id=1,context=msg_context)
            new_msg.save()
            print "新建消息成功！"
            # 微信消息
            client = fetch_wechatpy_client()
            client.message.send_text(openid,'恭喜%s: 成功充值%d元,您目前夺宝币余额是%d。请关注桔叶活动，会不定期有充值优惠活动~' % (customer.name,recharge_fee,account.balance_coins))
	return  HttpResponse(notify.returnXml())

# 订单微信支付回调
@csrf_exempt
@catch
def order_wechat_pay_notify_payback(request):
    duobao_logger = logging.getLogger('record')
    """支付回调"""
    xml = request.body
 
    #使用通用通知接口
    notify = Notify_pub()
    notify.saveData(xml)
    #验证签名，并回应微信。
    #对后台通知交互时，如果微信收到商户的应答不是成功或超时，微信认为通知失败，
    #微信会通过一定的策略（如30分钟共8次）定期重新发起通知，
    #尽可能提高通知的成功率，但微信不保证通知最终能成功
    if not notify.checkSign():
        print 'sign check failed!'
        notify.setReturnParameter("return_code", FAIL) #返回状态码
        notify.setReturnParameter("return_msg", "签名失败") #返回信息
    else:
        result = notify.getData()
        print 'pay back result', result
        openid = result["openid"]
        transaction_id = int(result["attach"])
        recharge_fee = int(result["total_fee"])
        customer = Customer.objects.get(openid=openid)        
        if result["return_code"] == FAIL:
            notify.setReturnParameter("return_code", FAIL)
            notify.setReturnParameter("return_msg", "通信错误")
            # 支付失败

            transaction = Transaction.objects.get(transaction_status_id=1,customer=customer)
            transaction.transaction_status_id=4
            for order in transaction.orders.all():
            	order.delete()
            transaction.save()   
            duobao_logger.info("[结算] 用户transaction结算失败,通信错误! transaction id为 %d" % transaction.id);         
            print '通信错误'
        elif result["result_code"] == FAIL:
            notify.setReturnParameter("return_code", FAIL)
            notify.setReturnParameter("return_msg", result["err_code_des"])
            # 支付失败
            transaction = Transaction.objects.get(transaction_status_id=1,customer=customer)
            transaction.transaction_status_id=4
            for order in transaction.orders.all():
            	order.delete()            
            transaction.save()
            duobao_logger.info("[结算] 用户transaction结算失败,result code错误! transaction id为 %d" % transaction.id);         
            print 'result code 错误'
        else:
            notify.setReturnParameter("return_code", SUCCESS)
            out_trade_no = result["out_trade_no"] #商户系统的订单号，与请求一致。	
            # 支付成功
            duobao_logger.info("[进入结算回调]用户名为%s,用户ID为%d" % (customer.name,customer.id))
            transaction = Transaction.objects.get(id=transaction_id)
            if transaction.transaction_status_id == 2:
            	duobao_logger.info("[进入结算回调]transaction id为 %d 已经经过计算! " % transaction.id)
            	return  HttpResponse(notify.returnXml())
            transaction.transaction_status_id=2
            transaction.save()
            duobao_logger.info("[结算] 用户transaction结算成功! transaction id为 %d" % transaction.id);         
            # 新建消息
            for order in transaction.orders.all():
            	order.order_status_id = 1
            	order.save()
            	duobao_logger.info("[结算] 用户订单结算成功! order id 为 %d " % order.id);
            	temp_take_part_price = 0
            	if order.item.merchant.mer_type == 3:
            		temp_take_part_price = order.order_times * 10
            	else:
            		temp_take_part_price = order.order_times
            	# msg_title = "参与夺宝成功"
            	# msg_context = "您成功参与\"%s的第%s期活动\"%d人次，并已经分配中奖号码。具体详情请进入夺宝记录查看~祝您获奖" % (order.item.merchant.name,order.item.item_code,temp_take_part_price)
            	# new_msg = NoticeMsg.objects.create(shop=order.item.merchant.shop,customer=customer,title=msg_title,notice_msg_status_id=1,context=msg_context)
            	# new_msg.save()

            	item_link = "http://2.juye51.com/shop/merchant_detail_info/?page_id=1&item_id=%d" % order.item.id 
            	record_link = "http://2.juye51.com/record/my_all_records/?shop_id=%d" % int(order.item.merchant.shop.id)
            	client = fetch_wechatpy_client()
            	client.message.send_text(customer.openid,"%s: \n您成功参与<a href='%s'>%s的第%s期活动</a>%d人次，并已经分配中奖号码。\n具体详情请<a href='%s'>进入夺宝记录</a>查看~祝您获奖" % (customer.name,item_link,order.item.merchant.name,order.item.item_code,temp_take_part_price,record_link))				            	

            # 处理orders
            orders = transaction.orders.all()
            for order in orders:
            	item = order.item            	
            	good_number = order.order_times
            	
            	if item.merchant.mer_type_id == 3:
            		item.take_part_num += 10 * good_number
            	else:
            		item.take_part_num += good_number

            	merchant_price = item.merchant.price    

            	# 分配奖券
            	ticket_number = good_number
            	if item.merchant.mer_type_id == 3:
            		ticket_number = good_number * 10	  	

            	duobao_logger.info("[结算分配奖券-微信支付] 对用户%s, 用户ID为%d ITEM_ID为%d 即将分配%d个奖券" % (customer.name,customer.id,item.id,ticket_number))		
            	# 查询已经分配的奖券
            	item_tickets = LotteryTicket.objects.filter(item=item)
            	item_ticket_numbers = []
            	for item_ticket in item_tickets:
            		item_ticket_numbers.append(item_ticket.ticket_no)
            	duobao_logger.info("[结算分配奖券-微信支付] 期号为%s的项目,已经参与了%d次,已经分配奖券%d张" % (item.item_code,item.take_part_num,len(item_tickets)))

            	for i in range(0,ticket_number):
            		random_ticket_no = random.randint(0,merchant_price-1)
            		# 直到找到未分配的奖券
            		while True:
            			tickets = LotteryTicket.objects.filter(item=item,ticket_no=random_ticket_no + 100000000)
            			if len(tickets) == 0:
            				new_ticket = LotteryTicket.objects.create(item=item,ticket_no=random_ticket_no + 100000000,order=order)
            				duobao_logger.info("[结算分配奖券-微信支付] 用户ID: %d 期号为%s的项目,成功分配第%d张奖券,号码为%s" % (customer.id,item.item_code,i+1,new_ticket.ticket_no))
            				break
            			else:
            				random_ticket_no = (random_ticket_no + 1) % merchant_price

            	# 如果本期商品结束，则修改状态（等待开奖）
            	if item.merchant.price == item.take_part_num:
            		item.item_status_id = 4
            		# 建立新的一期
            		if item.merchant.auto_up_shelve == True and item.item_type.id == 1: 
            			new_item = Item.objects.create(merchant=item.merchant,item_status_id=1,item_type_id=1)
            			new_item.item_code = str(100000000 + int(new_item.id))
            			new_item.save()						
            	item.save()            	          	
    return  HttpResponse(notify.returnXml())

@csrf_exempt
@catch
def test_payback(request):
    """支付回调"""
    xml = request.body
 
    #使用通用通知接口
    notify = Notify_pub()
    notify.saveData(xml)
    #验证签名，并回应微信。
    #对后台通知交互时，如果微信收到商户的应答不是成功或超时，微信认为通知失败，
    #微信会通过一定的策略（如30分钟共8次）定期重新发起通知，
    #尽可能提高通知的成功率，但微信不保证通知最终能成功
    if not notify.checkSign():
        print 'sign check failed!'
        notify.setReturnParameter("return_code", FAIL) #返回状态码
        notify.setReturnParameter("return_msg", "签名失败") #返回信息
    else:
        result = notify.getData()
        print 'pay back result', result
        openid = result["openid"]
        recharge_fee = int(result["total_fee"])
        customer = Customer.objects.get(openid=openid)        
        if result["return_code"] == FAIL:
            notify.setReturnParameter("return_code", FAIL)
            notify.setReturnParameter("return_msg", "通信错误")          
            print '通信错误'
        elif result["result_code"] == FAIL:
            notify.setReturnParameter("return_code", FAIL)
            notify.setReturnParameter("return_msg", result["err_code_des"])
            # 支付失败)            
            print 'result code 错误'
        else:
            notify.setReturnParameter("return_code", SUCCESS)
            out_trade_no = result["out_trade_no"] #商户系统的订单号，与请求一致。	
            # 支付成功

	return  HttpResponse(notify.returnXml())

# 完善个人信息页
def imporve_personal_info(request):
	return render(request,'web/user/imporve_personal_info.html')

# 我的红包页
def my_redpack(request):
	return render(request,'web/user/my_redpack.html')

# 中奖记录
def win_record(request):
	return render(request,'web/user/win_record.html')

# 最近揭晓
def recent_announce(request):
	return render(request,'web/user/recent_announce.html')

# 我的消息
@sns_userinfo
def my_message(request):
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']

	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']

	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 

	# 查看用户是否存在
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		if invest_customer != None:
			customer.investor_id = invest_customer.id
		customer.save()
	else:
		customer = customers[0]
		account = customer.account	

	shop_id = request.GET['shop_id']
	shop = Shop.objects.get(id=int(shop_id))
	# 将session中的message置为已读
	my_have_read_message_list = []
	if 'message_list' in request.session:
		my_have_read_message_list = request.session['message_list']

	for message_id in my_have_read_message_list:
		my_have_read_message = NoticeMsg.objects.get(id=int(message_id))
		my_have_read_message.notice_msg_status_id = 2
		my_have_read_message.save()
	request.session['message_list'] = []	# 置空消息		
	# 消息置为已读结束

	my_messages = NoticeMsg.objects.filter(customer=customer,shop=shop) | NoticeMsg.objects.filter(customer=customer,shop=None)
	my_messages = my_messages.order_by('-create_time')
	# 将这些message加入到session中，标记为已读消息
	message_list = []
	if 'message_list' in request.session:
		message_list = request.session['message_list']
	for my_message in my_messages:
		if my_message.id not in message_list:
			message_list.append(my_message.id)
	request.session['message_list'] = message_list

	return render(request,'web/user/my_message.html',{"shop_id":shop_id,"my_messages":my_messages})


# 邀请页面
@sns_userinfo
def my_invest_page(request):
	# 信息同步
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']	
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']

	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 

	# 查看用户是否存在
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account	

	# 生成邀请链接
	short_link_serv = "http://50r.cn/short_url.json?url="
	invest_url = "http://2.juye51.com/user/selfinfo/?investor_openid=" + openid
	# 生成短连接
	request_result = urllib.urlopen(short_link_serv + invest_url).read()
	invest_short_link = json.loads(request_result)['url']
	# 二维码图片地址
	qr_code_img_addr = "http://qr.liantu.com/api.php?text=" + invest_short_link
	return render(request,'web/user/my_invest_page.html',{"invest_link":invest_short_link,"qr_code_img_addr":qr_code_img_addr})


# 配送地址管理
@sns_userinfo
def recieve_address(request):
	# 信息同步
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo

	shop_id = int(request.GET['shop_id'])
	openid = request.session['openid']
	userinfo = request.session['userinfo']	
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']

	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 

	# 查看用户是否存在
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account		
	logger = logging.getLogger('default')
	logger.info("customer id :%d, shop_id : %d" % (customer.id,shop_id))		
	addr_objs = Address.objects.filter(customer=customer)
	# 将session中的message置为已读
	my_have_read_message_list = []
	if 'message_list' in request.session:
		my_have_read_message_list = request.session['message_list']

	for message_id in my_have_read_message_list:
		my_have_read_message = NoticeMsg.objects.get(id=int(message_id))
		my_have_read_message.notice_msg_status_id = 2
		my_have_read_message.save()
	request.session['message_list'] = []	# 置空消息		
	# 消息置为已读结束
	return render(request,'web/user/recieve_address.html',{"addrs":addr_objs,'shop_id':shop_id})

# 新增配送地址
@sns_userinfo
def add_new_address(request):
	# 信息同步
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	shop_id = int(request.GET['shop_id'])
	openid = request.session['openid']
	userinfo = request.session['userinfo']	
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']

	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 

	# 查看用户是否存在
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account	
	return render(request,'web/user/add_new_address.html',{'shop_id':shop_id})	

# 提交地址表单
@sns_userinfo
@csrf_exempt
def submit_address(request):
	# 信息同步
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']
	shop_id = None
	if 'shop_id' in request.GET:
		shop_id = int(request.GET['shop_id'])
	else:
		shop_id = int(request.POST['shop_id'])
	print shop_id,"shop_id"
	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 

	# 获取用户
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account

	response = {'status':0}
	addr_dict = request.POST
	name = addr_dict['consignee']
	mobile = addr_dict['mobile']
	zipcode = addr_dict['zip']
	address = addr_dict['address']
	province_code = addr_dict['region_lv2']
	city_code = addr_dict['region_lv3']
	district_code = addr_dict['region_lv4']
	province_name = None
	city_name = None
	district_name = None
	if name == "" or mobile == "" or zipcode == "" or address == "" or province_code == 0 or city_code == 0 or district_code == 0:
		response['info'] = "信息不完整，请完善地址信息"
	else:
		province_name = AddrInfo.objects.get(code=province_code).addr
		city_name = AddrInfo.objects.get(code=city_code).addr
		district_name = AddrInfo.objects.get(code=district_code).addr
		addr_obj = Address.objects.create(customer=customer,name=name,province=province_name,
			city=city_name,district=district_name,detail_address=address,postcode=zipcode,mobile=mobile)
		addr_obj.save()
		if len(Address.objects.filter(customer=customer,is_default_addr=1)) == 0:
			addr_obj.is_default_addr = 1
			addr_obj.save()
		# print province_name,city_name,district_name
		response = {'status':1,'url':'/user/recieve_address/?shop_id=%d' % shop_id} 
	# {status: 1, url: "/wap/index.php?show_prog=1"} 成功
	
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 设置默认收货地址
@sns_userinfo
@csrf_exempt
def set_default_address(request):
	shop_id = None
	if 'shop_id' in request.GET:
		shop_id = int(request.GET['shop_id'])
	else:
		shop_id = int(request.POST['shop_id'])
	addr_id = request.GET['addr_id']
	print "修改地址id",addr_id
	addr_obj = Address.objects.get(id=int(addr_id))
	
	customer = addr_obj.customer
	cus_addr_objs = Address.objects.filter(customer=customer) 
	for cus_addr_obj in cus_addr_objs:
		cus_addr_obj.is_default_addr = 0
		cus_addr_obj.save()
	addr_obj.is_default_addr = 1 # 设为默认地址
	addr_obj.save()
	response = {'status':1,'url':'/user/recieve_address/?shop_id=%d' % shop_id}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))



# 设置默认收货地址
@sns_userinfo
@csrf_exempt
def delete_address(request):
	shop_id = None
	if 'shop_id' in request.GET:
		shop_id = int(request.GET['shop_id'])
	else:
		shop_id = int(request.POST['shop_id'])	
	addr_id = request.GET['addr_id']
	# print "修改地址id",addr_id
	Address.objects.get(id=int(addr_id)).delete()	
	response = {'status':1,'url':'/user/recieve_address/?shop_id=%d' % shop_id}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

###############################################################
#
#             订单模块
# 
###############################################################
@sns_userinfo
@csrf_exempt
def my_all_records(request):
	# 信息同步
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']

	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 

	# 获取用户
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account

	# 获取shop信息
	shop_id = None
	if 'shop_id' in request.GET:
		shop_id = request.GET['shop_id']
	elif 'shop_id' in request.POST:
		shop_id = request.POST['shop_id']

	# if shop_id == None:
	# 	if customer.last_login_shop:
	# 		shop_id = customer.last_login_shop.id
	# print "shop_id = ",shop_id
	# if customer.last_login_shop == None:
	# 	customer.last_login_shop = Shop.objects.get(id=shop_id)
	# 	customer.save()
	# elif shop_id != customer.last_login_shop.id:
	# 	customer.last_login_shop = Shop.objects.get(id=shop_id)
	# 	customer.save()		
	# 获取shop信息结束

	# 查看session购物车的内容
	cart_list = {}
	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']	
	cart_good_number = 0
	# new_cart_list = {} # 过滤后的购物车
	for item_id in cart_list:
		item = Item.objects.get(id=item_id)
		if int(item.merchant.shop_id) != int(shop_id):
			continue
		cart_good_number += cart_list[item_id]


	# 将session中的message置为已读
	my_have_read_message_list = []
	if 'message_list' in request.session:
		my_have_read_message_list = request.session['message_list']

	for message_id in my_have_read_message_list:
		my_have_read_message = NoticeMsg.objects.get(id=int(message_id))
		my_have_read_message.notice_msg_status_id = 2
		my_have_read_message.save()
	request.session['message_list'] = []	# 置空消息		
	# 消息置为已读结束

	# transactions = Transaction.objects.filter(customer=customer,transaction_status_id=2)

	page_id = 1
	page_length = 10
	if "page_id" in request.GET:
		page_id = int(request.GET['page_id'])
	elif "page_id" in request.POST:
		page_id = int(request.POST['page_id'])

	if "page_length" in request.GET:
		page_length = int(request.GET['page_length']) 
	elif "page_length" in request.POST:
		page_length = int(request.POST['page_length'])

	all_item_order_records = {}
	orders = Order.objects.filter(customer=customer,item__merchant__shop_id=shop_id).exclude(item__item_status_id=3).exclude(order_status_id=5).exclude(order_status_id=3)  # 排除已取消
	# for transaction in transactions:
	# orders = transaction.orders.all()
	for order in orders:
		item = order.item
		if int(item.merchant.shop_id) != int(shop_id): # 保证order是本商店的
			continue
		order_times = 0
		if item.merchant.mer_type_id == 3:
			order_times = 10 * int(order.order_times)
		else:
			order_times = int(order.order_times)		
		print order_times
		if item in all_item_order_records:
			all_item_order_records[item]["my_order_times"] += order_times
		else:
			all_item_order_records[item] = {"my_order_times":order_times,"surplus_order_times":item.merchant.price - item.take_part_num,
			"item_progress":float(item.take_part_num)/float(item.merchant.price) * 100.0}
			if item.item_status_id == 2:
				print item.winner_code,"中奖号码"
				print item.id
				all_item_order_records[item]['lottery_customer'] = LotteryTicket.objects.get(ticket_no=item.winner_code,item=item).order.customer		
	# 分页
	# all_item_order_records = all_item_order_records[page_id*page_length:(page_id+1)*page_length]
	# 排序，按照update time排序
	all_item_order_records = sorted(all_item_order_records.iteritems(), key=lambda d:d[0].update_time, reverse = True)
	processing_items = []
	announce_items = []
	finish_items = []
	for temp_item_record in all_item_order_records:
		if temp_item_record[0].item_status.id == 4:
			announce_items.append(temp_item_record)
		elif temp_item_record[0].item_status.id == 1:
			processing_items.append(temp_item_record)
		else:
			finish_items.append(temp_item_record)
	
	all_item_order_records = announce_items + processing_items + finish_items
	all_item_order_list = []

	order_records = {}
	order_item_index = 0
	for item in all_item_order_records:
		if order_item_index < (page_id - 1) * page_length:
			order_item_index += 1
			continue
		elif order_item_index >= page_id * page_length:
			break
		all_item_order_list.append(item)
		# order_records[item[0]] = item[1]
		order_item_index += 1

	next_page_id = page_id + 1
	if order_item_index > page_id * page_length or order_item_index == 0: #没有下一页
		next_page_id = -1
	print page_id,page_length
	# print order_records
	return render(request,'web/user/my_all_records.html',{"order_records":order_records,'all_item_order_list':all_item_order_list,
		'cart_good_number':cart_good_number,'next_page_id':next_page_id,'current_page_id':page_id,
	'shop_id':shop_id})

# 进行中的订单
@sns_userinfo
@csrf_exempt
def my_processing_records(request):
	# 信息同步
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']

	nickname = return_unicode_nickname(nickname)
	# 获取用户
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account


	# 获取shop信息
	shop_id = None
	if 'shop_id' in request.GET:
		shop_id = request.GET['shop_id']
	elif 'shop_id' in request.POST:
		shop_id = request.POST['shop_id']

	# if shop_id == None:
	# 	if customer.last_login_shop:
	# 		shop_id = customer.last_login_shop.id

	# if customer.last_login_shop == None:
	# 	customer.last_login_shop = Shop.objects.get(id=shop_id)
	# 	customer.save()
	# elif shop_id != customer.last_login_shop.id:
	# 	customer.last_login_shop = Shop.objects.get(id=shop_id)
	# 	customer.save()		
	# 获取shop信息结束

	# 查看session购物车的内容
	cart_list = {}
	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']	
	cart_good_number = 0
	# new_cart_list = {} # 过滤后的购物车
	for item_id in cart_list:
		item = Item.objects.get(id=item_id)
		if int(item.merchant.shop_id) != int(shop_id):
			continue
		cart_good_number += cart_list[item_id]

	# 将session中的message置为已读
	my_have_read_message_list = []
	if 'message_list' in request.session:
		my_have_read_message_list = request.session['message_list']

	for message_id in my_have_read_message_list:
		my_have_read_message = NoticeMsg.objects.get(id=int(message_id))
		my_have_read_message.notice_msg_status_id = 2
		my_have_read_message.save()
	request.session['message_list'] = []	# 置空消息		
	# 消息置为已读结束
	# transactions = Transaction.objects.filter(customer=customer,transaction_status_id=2)

	page_id = 1
	page_length = 10
	if "page_id" in request.GET:
		page_id = int(request.GET['page_id'])
	elif "page_id" in request.POST:
		page_id = int(request.POST['page_id'])

	if "page_length" in request.GET:
		page_length = int(request.GET['page_length']) 
	elif "page_length" in request.POST:
		page_length = int(request.POST['page_length'])



	# 取出所有进行中的orders
	orders = Order.objects.filter(customer=customer,item__item_status_id=1,item__merchant__shop_id=shop_id).exclude(order_status_id=5).exclude(order_status_id=3)
	all_item_order_records = {}
	all_item_order_list = []
	for order in orders:
		# if order.order_status_id != 1:
		# 	continue
		item = order.item
		if item.merchant.shop_id == shop_id: # 保证order是本商店的
			continue			
		if item.item_status_id != 1:
			continue
		order_times = 0
		if item.merchant.mer_type_id == 3:
			order_times = 10 * int(order.order_times)
		else:
			order_times = int(order.order_times)		

		if item in all_item_order_records:
			all_item_order_records[item]["my_order_times"] += order_times
		else:
			all_item_order_records[item] = {"my_order_times":order_times,"surplus_order_times":item.merchant.price - item.take_part_num,
			"item_progress":float(item.take_part_num)/float(item.merchant.price) * 100.0}

	# 分页
	# all_item_order_records = all_item_order_records[page_id*page_length:(page_id+1)*page_length]
	# 排序
	all_item_order_records = sorted(all_item_order_records.iteritems(), key=lambda d:d[0].update_time, reverse = True)
	order_records = {}
	order_item_index = 0
	for item in all_item_order_records:
		if order_item_index < (page_id - 1) * page_length:
			order_item_index += 1
			continue
		elif order_item_index >= page_id * page_length:
			break
		# order_records[item] = all_item_order_records[item]
		all_item_order_list.append(item)
		order_item_index += 1
	next_page_id = page_id + 1
	if order_item_index > page_id * page_length or order_item_index == 0: #没有下一页
		next_page_id = -1
	# print page_id,page_length
	# print order_records

	return render(request,'web/user/my_processing_records.html',{"order_records":order_records,'all_item_order_list':all_item_order_list,
		'cart_good_number':cart_good_number,'next_page_id':next_page_id,'current_page_id':page_id,'shop_id':shop_id})	

# 已经揭晓的订单
@sns_userinfo
@csrf_exempt
def my_over_records(request):
	# 信息同步
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']

	nickname = return_unicode_nickname(nickname)

	# 获取用户
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account

	page_id = 1
	page_length = 10
	if "page_id" in request.GET:
		page_id = int(request.GET['page_id'])
	elif "page_id" in request.POST:
		page_id = int(request.POST['page_id'])

	if "page_length" in request.GET:
		page_length = int(request.GET['page_length']) 
	elif "page_length" in request.POST:
		page_length = int(request.POST['page_length'])


	# 获取shop信息
	shop_id = None
	if 'shop_id' in request.GET:
		shop_id = request.GET['shop_id']

	# if shop_id == None:
	# 	if customer.last_login_shop:
	# 		shop_id = customer.last_login_shop.id

	# if customer.last_login_shop == None:
	# 	customer.last_login_shop = Shop.objects.get(id=shop_id)
	# 	customer.save()
	# elif shop_id != customer.last_login_shop.id:
	# 	customer.last_login_shop = Shop.objects.get(id=shop_id)
	# 	customer.save()		
	# 获取shop信息结束


	# 查看session购物车的内容
	cart_list = {}
	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']	
	cart_good_number = 0
	# new_cart_list = {} # 过滤后的购物车
	for item_id in cart_list:
		item = Item.objects.get(id=item_id)
		if int(item.merchant.shop_id) != int(shop_id):
			continue
		cart_good_number += cart_list[item_id]

	# 将session中的message置为已读
	my_have_read_message_list = []
	if 'message_list' in request.session:
		my_have_read_message_list = request.session['message_list']

	for message_id in my_have_read_message_list:
		my_have_read_message = NoticeMsg.objects.get(id=int(message_id))
		my_have_read_message.notice_msg_status_id = 2
		my_have_read_message.save()
	request.session['message_list'] = []	# 置空消息		
	# 消息置为已读结束

	# transactions = Transaction.objects.filter(customer=customer,transaction_status_id=2)
	orders = Order.objects.filter(customer=customer,item__item_status_id=2,item__merchant__shop_id=shop_id) | Order.objects.filter(customer=customer,item__item_status_id=5,item__merchant__shop_id=shop_id) | Order.objects.filter(customer=customer,item__item_status_id=6,item__merchant__shop_id=shop_id).exclude(order_status_id=5).exclude(order_status_id=3)
	all_item_order_records = {}
	# for transaction in transactions:
	# orders = transaction.orders.all()
	for order in orders:
		# if order.order_status_id != 1:
		# 	continue
		item = order.item
		if item.merchant.shop_id == shop_id: # 保证order是本商店的
			continue			
		if item.item_status_id != 2: # 结束的item（已经揭晓的）
			continue
		# 获取获奖号码
		winner_code = item.winner_code
		lottery_tickets = LotteryTicket.objects.filter(ticket_no=winner_code,item=item)
		if len(lottery_tickets) == 0:
			print winner_code,item.id,item.merchant.name
			print "未查到此中奖号码！"
			continue
		lottery_ticket = lottery_tickets[0]

		order_times = 0
		if item.merchant.mer_type_id == 3:
			order_times = 10 * int(order.order_times)
		else:
			order_times = int(order.order_times)		

		if item in all_item_order_records:
			all_item_order_records[item]["my_order_times"] += order_times
		else:
			all_item_order_records[item] = {"my_order_times":order_times,"surplus_order_times":item.merchant.price - item.take_part_num,
			"item_progress":float(item.take_part_num)/float(item.merchant.price) * 100.0,"lottery_order":lottery_ticket.order}

	# 分页
	order_records = {}
	order_item_index = 0
	for item in all_item_order_records:
		if order_item_index < (page_id - 1) * page_length:
			order_item_index += 1
			continue
		elif order_item_index >= page_id * page_length:
			break
		order_records[item] = all_item_order_records[item]
		order_item_index += 1
	next_page_id = page_id + 1
	if order_item_index > page_id * page_length or order_item_index == 0: #没有下一页
		next_page_id = -1	

	return render(request,'web/user/my_over_records.html',{"order_records":order_records,'cart_good_number':cart_good_number,
		'shop_id':shop_id,'current_page_id':page_id,'next_page_id':next_page_id})	

# 我的中奖记录
@sns_userinfo
@csrf_exempt
def my_winning_records(request):
	# 信息同步
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']

	nickname = return_unicode_nickname(nickname)

	# 获取用户
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account


	# 获取shop信息
	shop_id = None
	if 'shop_id' in request.GET:
		shop_id = request.GET['shop_id']
	elif 'shop_id' in request.POST:
		shop_id = request.POST['shop_id']

	# if shop_id == None:
	# 	if customer.last_login_shop:
	# 		shop_id = customer.last_login_shop.id

	# if customer.last_login_shop == None:
	# 	customer.last_login_shop = Shop.objects.get(id=shop_id)
	# 	customer.save()
	# elif shop_id != customer.last_login_shop.id:
	# 	customer.last_login_shop = Shop.objects.get(id=shop_id)
	# 	customer.save()		
	# 获取shop信息结束

	# 查看当前用户是否提交过默认地址
	default_addrs = Address.objects.filter(customer=customer,is_default_addr=1)
	# 查看session购物车的内容
	cart_list = {}
	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']	
	cart_good_number = 0
	# new_cart_list = {} # 过滤后的购物车
	for item_id in cart_list:
		item = Item.objects.get(id=item_id)
		if int(item.merchant.shop_id) != int(shop_id):
			continue
		cart_good_number += cart_list[item_id]

	# 将session中的message置为已读
	my_have_read_message_list = []
	if 'message_list' in request.session:
		my_have_read_message_list = request.session['message_list']

	for message_id in my_have_read_message_list:
		my_have_read_message = NoticeMsg.objects.get(id=int(message_id))
		my_have_read_message.notice_msg_status_id = 2
		my_have_read_message.save()
	request.session['message_list'] = []	# 置空消息		
	# 消息置为已读结束

	# transactions = Transaction.objects.filter(customer=customer,transaction_status_id=2)

	page_id = 1
	page_length = 10
	if "page_id" in request.GET:
		page_id = int(request.GET['page_id'])
	elif "page_id" in request.POST:
		page_id = int(request.POST['page_id'])

	if "page_length" in request.GET:
		page_length = int(request.GET['page_length']) 
	elif "page_length" in request.POST:
		page_length = int(request.POST['page_length'])

	# 查询所有本人中奖的item

	my_winning_items = Item.objects.filter(item_status_id=2,merchant__shop_id=shop_id) | Item.objects.filter(item_status_id=5,merchant__shop_id=shop_id) | Item.objects.filter(item_status_id=6,merchant__shop_id=shop_id)
	my_winning_results = []
	for winning_item in my_winning_items:
		if len(LotteryTicket.objects.filter(item=winning_item,ticket_no=winning_item.winner_code,order__customer=customer)) == 0:
			continue
		else:
			# print "winning item info " , winning_item.id, winning_item.winner_code,customer.id
			my_winning_results.append(winning_item)
	my_winning_results = my_winning_results[(page_id-1)*page_length:page_id*page_length]

	if len(my_winning_results) > page_id*page_length:
		next_page_id  = page_id + 1
	else:
		next_page_id = -1

	return render(request,'web/record/my_winning_records.html',{"my_winning_items":my_winning_results,'cart_good_number':cart_good_number,
		'shop_id':shop_id,'current_page_id':page_id,'next_page_id':next_page_id,"customer":customer,"default_addrs_length":len(default_addrs)})	

# 用户领奖
def accept_reward(request):
	item_id = int(request.GET['item_id'])
	item = Item.objects.get(id=item_id)
	item.item_status_id = 5
	item.save()
	shop_id = item.merchant.shop.id
	return HttpResponseRedirect('/record/my_winning_records/?shop_id=%d' % shop_id)


# 商品详情页新增订单
@csrf_exempt
def merchant_add_order(request):
	# response = {'status':1,'url':'/index/'}
	print "merchant_add_order"
	item_id = request.POST['data_id']
	item_by_num = int(request.POST['buy_num'])
	item = Item.objects.get(id=item_id)
	# print item_by_num,item.merchant.mer_type_id

	if item.merchant.mer_type_id == 3:
		item_by_num = item_by_num / 10
	cart_list = {}
	print item_by_num,item.merchant.mer_type_id
	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']

	if item_id in cart_list:
		cart_list[item_id] += item_by_num
	else:
		cart_list[item_id] = item_by_num

	cart_total_number = 0 # 购物车总共的商品数
	# if 'cart_total_number' in request.session:
	# 	cart_total_number = int(request.session['cart_total_number'])

	for key in cart_list:
		cart_total_number += cart_list[key]

	request.session['cart_total_number'] = cart_total_number
	request.session['cart_list'] = cart_list

	response = {"status":1,"info":"\u5df2\u52a0\u5165\u6e05\u5355","cart_item_num":10,"jump":"\/index\/"}
	# 
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	


# 中奖详情页面
def winning_detail(request):
	return render(request,'web/record/winning_detail.html')


# 我的本期号码
@sns_userinfo
def my_item_tickets(request):
	# 信息同步
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']

	nickname = return_unicode_nickname(nickname)

	# 获取用户
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account

	item_id = None	
	if "item_id" in request.POST:
		item_id = int(request.POST['item_id'])
	else:
		item_id = int(request.GET['item_id'])
	item = Item.objects.get(id=item_id)
	shop_id = item.merchant.shop_id
	lottery_tickets = LotteryTicket.objects.filter(item=item,order__customer=customer)
	ticket_number = len(lottery_tickets)
	# ,{'item':item,'lottery_tickets':lottery_tickets}
	return render(request,'web/record/my_item_tickets.html',{'item':item,'lottery_tickets':lottery_tickets,'shop_id':shop_id,
		'ticket_number':ticket_number})


# 计算中奖详情
def calculate_winning_detail(request):
	shop_id = int(request.GET['shop_id'])
	item_id = int(request.GET['item_id'])
	item = Item.objects.get(id=item_id)

	# 查看session购物车的内容
	cart_list = {}
	if 'cart_list' not in request.session:
		cart_list = {}
	else:
		cart_list = request.session['cart_list']	
	cart_good_number = 0
	new_cart_list = {} # 过滤后的购物车
	for cart_item_id in cart_list:
		cart_item = Item.objects.get(id=cart_item_id)
		if int(cart_item.merchant.shop_id) != int(shop_id):
			continue
		cart_good_number += cart_list[cart_item_id]

	lottery_tickets = list(LotteryTicket.objects.filter(item=item).order_by('create_time'))
	# 取末尾50条数据
	lottery_tickets = lottery_tickets[-50:]		
	total_sum = 0
	lottery_ticket_infos = []
	for lottery_ticket in lottery_tickets:
		temp_lottery_ticket_info = {}
		ticket_createtime = lottery_ticket.create_time
		ticket_createtime_str = ticket_createtime.strftime("%H%M%S")
		ticket_createtime_int = int(ticket_createtime_str)
		temp_lottery_ticket_info['customer'] = lottery_ticket.order.customer.name
		temp_lottery_ticket_info['timestr'] = ticket_createtime.strftime("%Y-%m-%d %H:%M:%S")
		temp_lottery_ticket_info['timeint'] = ticket_createtime_int
		lottery_ticket_infos.append(temp_lottery_ticket_info)
		total_sum += ticket_createtime_int
	total_sum_A = total_sum
	print item.winner_lottery_result,"item.winner_lottery_result"
	total_sum += int(item.winner_lottery_result)	
	return render(request,'web/record/calculate_winning_detail.html',
		{'lottery_ticket_infos':lottery_ticket_infos,'total_sum':total_sum,
		'winner_lottery_result':item.winner_lottery_result,"item":item,
		"total_sum_A":total_sum_A,"shop_id":shop_id,"cart_good_number":cart_good_number})

###############################################################
#
#             help模块
# 
###############################################################
def helpindex(request):
	shop_id = int(request.GET['shop_id'])
	return render(request,'web/help/help_index.html',{'shop_id':shop_id})	

# 了解一元夺宝
def liaojie_duobao(request):
	shop_id = int(request.GET['shop_id'])
	return render(request,'web/help/liaojie_duobao.html',{'shop_id':shop_id})	

# 一元夺宝协议
def agreement(request):
	shop_id = int(request.GET['shop_id'])
	return render(request,'web/help/agreement.html',{'shop_id':shop_id})	

# 常见问题
def common_question(request):
	shop_id = int(request.GET['shop_id'])
	return render(request,'web/help/common_question.html',{'shop_id':shop_id})

# 商品配送
def shop_delivery(request):
	shop_id = int(request.GET['shop_id'])
	return render(request,'web/help/shop_delivery.html',{'shop_id':shop_id})

def test(request):
	return render(request,'web/user/self_customer_service.html')

@catch
def caonima(request):
	return render(request,'web/user/wechat_pay_test.html')


@catch
@csrf_exempt
def wechat_tester_req(request):
	"""获取支付信息"""
	# if 'openid' not in request.session:
	# 	if request.openid != None:
	# 		request.session['openid'] = request.openid

	# openid = request.session['openid']
	money = int(request.POST['money']) * 100 # 单位是元
	# print money
	jsApi = JsApi_pub()
	time_unify_start = time.time()	
	unifiedOrder = UnifiedOrder_pub()
	unifiedOrder.setParameter("openid","oTPeLwaIOjcJC1KSPKTvH_Xe28Wk") #商品描述
	unifiedOrder.setParameter("body","红包接龙活动") #商品描述
	timeStamp = time.time()
	# print 'unifiedOrder time delta ', timeStamp - time_unify_start
	out_trade_no = "{0}{1}".format(WxPayConf_pub.APPID, int(timeStamp*100))
	unifiedOrder.setParameter("out_trade_no", out_trade_no) #商户订单号
	unifiedOrder.setParameter("total_fee", str(money)) #总金额
	unifiedOrder.setParameter("notify_url", WxPayConf_pub.TEST_NOTIFY_URL) #通知地址 
	unifiedOrder.setParameter("trade_type", "JSAPI") #交易类型
	unifiedOrder.setParameter("attach", "juye_tech") #附件数据，可分辨不同商家(string(127))	

	time_unify_end = time.time()
	try:
		prepay_id = unifiedOrder.getPrepayId()
		jsApi.setPrepayId(prepay_id)
		jsApiParameters = jsApi.getParameters()
		# print prepay_id,'prepay_id'
		# print 'pay detail end function delta!!!', time_unify_end - time_paydetail_start
	except Exception as e:
		print(e)
	else:
		# print jsApiParameters
		return HttpResponse(jsApiParameters)

	# return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

################################################################
#
# 线下跑批
#
################################################################
def lottery_result_batch(request):
	response = {}
	page_link = "http://kjh.cailele.com/kj_ssc.shtml"
	r = urllib2.Request(page_link)
	f = urllib2.urlopen(r, data=None, timeout=10)
	soup = BeautifulSoup(f.read(),"html.parser")
	# print soup
	current_date_tag = soup.find('p',{"class":"cz_name_period"})
	current_date_str = str(current_date_tag.text)
	print current_date_str
	lottery_table_results = soup.findAll('table',{"class":"stripe"})
	lottery_results = []
	for lottery_table_result in lottery_table_results:
		tmp_lottery_results = lottery_table_result.findAll("tr")[1:]
		for tmp_lottery_result in tmp_lottery_results:
			tds = tmp_lottery_result.findAll("td")
			if tds[1].text == "" or len(tds[1].text) == 0:
				continue
			else:
				lottery_results.append(tmp_lottery_result)


	if len(lottery_results) == 0:
		return
	# 只拿最后一条
	lastest_lottery_result = lottery_results[-1]
	lastest_issue_no = current_date_str + lastest_lottery_result.findAll("td")[0].text
	lastest_result = lastest_lottery_result.findAll("td")[1].text.replace(",","")	
	lottery_db_select_result = LotteryResult.objects.filter(issue_no=lastest_issue_no,result=lastest_result)
	print lastest_issue_no,lastest_result
	last_lottery = None
	if len(lottery_db_select_result) == 0:
		# 新开奖
		last_lottery = LotteryResult.objects.create(issue_no=lastest_issue_no,result=lastest_result)
		last_lottery.save()
		# 离线跑批兑奖
		# cal_winning_result(db,lastest_issue_no,lastest_result)
		# write_record_db(db,record,'yiyuanduobao_shop_lotteryresult')
	else:
		print "record exist!!"	
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 离线跑批
	# 获取等待开奖的item
	waiting_lottery_items = Item.objects.filter(item_status_id=4)
	record_logger = logging.getLogger('record')
	for waiting_lottery_item in waiting_lottery_items:
		item_id = waiting_lottery_item.id
		item = Item.objects.get(id=item_id)
		merchant_id = waiting_lottery_item.merchant.id
		# 获取商品信息
		merchant_info = Merchant.objects.get(id=merchant_id)
		merchant_price = merchant_info.price
		# 获取项目对应的所有奖券
		lottery_tickets = list(LotteryTicket.objects.filter(item=item).order_by('create_time'))
		# 取末尾50条数据
		lottery_tickets = lottery_tickets[-50:]		
		total_sum = 0
		for lottery_ticket in lottery_tickets:
			ticket_createtime = lottery_ticket.create_time
			ticket_createtime_str = ticket_createtime.strftime("%H%M%S")
			ticket_createtime_int = int(ticket_createtime_str)
			total_sum += ticket_createtime_int
		total_sum += int(lastest_result)
		winning_ticket = 100000000 + total_sum % merchant_price
		# 记录中奖信息
		item.winner_lottery_result = lastest_result
		item.item_status_id = 2
		item.winner_code = winning_ticket
		try:
			item.lottery_time = datetime.datetime.now()
		except:
			item.lottery_time = datetime.now()
		
		# 中奖用户
		winner_customer = None
		try:
			record_logger.info("期号为 %s 的商品 %s 开奖,中奖号码为 %s" % (item.item_code,item.merchant.name,winning_ticket))
			winner_customer = LotteryTicket.objects.get(ticket_no=winning_ticket,item=item).order.customer
			record_logger.info("期号为 %s 的商品 %s 开奖结果, 中奖人id为 %d , 中奖人姓名 %s" % (item.item_code,item.merchant.name,winner_customer.id,winner_customer.name))
		except:
			print winning_ticket,"找不到 itemid = ",item.id
			record_logger.info("期号为 %s 的商品 %s 未查到中奖人!" % (item.item_code,item.merchant.name))
			continue
		item.winner_customer = winner_customer
		item.save()
		# 新建代卖消息
		msg_title = '恭喜您中奖啦'
		msg_context = "恭喜您中奖啦，您参与的\"%s\"期号为%s中奖啦，中奖期号为%s，请保证配送地址已经上传，并设置为默认，并保证配送地址中的电话保证畅通。" % (item.merchant.name,item.item_code,winning_ticket)
		new_msg = NoticeMsg.objects.create(shop=item.merchant.shop,customer=winner_customer,title=msg_title,notice_msg_status_id=1,context=msg_context)	
		new_msg.save()			
		# 新建消息结束		

		# 新建微信回复消息
		address_objs = Address.objects.filter(customer=winner_customer,is_default_addr=1)
		item_link = "http://2.juye51.com/shop/merchant_detail_info/?page_id=1&item_id=%d" % item.id 
		record_link = "http://2.juye51.com/record/my_all_records/?shop_id=%d" % int(item.merchant.shop.id)
		address_link = "http://2.juye51.com/user/recieve_address/?shop_id=%d" % int(item.merchant.shop.id)
		accept_reward_link = "http://2.juye51.com/record/accept_reward/?item_id=%d" % item.id 
		client = fetch_wechatpy_client()
		if len(address_objs) == 0:
			for i in range(0,3):
				try:
					client.message.send_text(winner_customer.openid,"中奖通知：\n %s: 恭喜您中奖啦，您参与的<a href='%s'>\"%s\" 第%s期</a> 中奖啦，中奖号码为%s。\n 您还未上传收货地址，<a href='%s'>点此填写收货地址，并设置为默认</a> \n\n <a href='%s'>------> 点击此处领奖</a>" % (winner_customer.name,item_link,item.merchant.name,item.item_code,winning_ticket,address_link,accept_reward_link))				            			
					break
				except:
					print "发送失败"
					continue
		else:
			address = address_objs[0]
			address_info = address.province + " " + address.city + " " + address.district + " " + address.detail_address
			address_postcode = address.postcode
			address_mobile = address.mobile
			for i in range(0,3):
				try:
					client.message.send_text(winner_customer.openid,"中奖通知：\n %s: 恭喜您中奖啦，您参与的<a href='%s'>\"%s\" 第%s期</a> 中奖啦，中奖号码为%s。\n\n 邮寄地址：%s\n 邮政编码：%s\n 收货人姓名：%s\n 收货人电话： %s \n <a href='%s'>------>点此领奖</a>" % (winner_customer.name,item_link,item.merchant.name,item.item_code,winning_ticket,address_info,address_postcode,address.name,address.mobile,accept_reward_link))
					break
				except:
					print "发送失败"
					continue

		print "新建消息！"
		print winning_ticket
		
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

################################################################
#
#  jssdk方法
#
################################################################

# 获取jsapi signature方法
@csrf_exempt
@catch
def get_proxy_selling_jsapi_signature(request):
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
    current_url = request.session['proxy_selling_url']
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


@csrf_exempt
@catch
def get_merchant_detail_info_jsapi_signature(request):
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
    current_url = request.session['merchant_detail_info_url']
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

@sns_userinfo
@csrf_exempt
@catch
def share_new_item(request):
	# 信息同步
	if 'openid' not in request.session:
		if request.openid != None:
			request.session['openid'] = request.openid
	if 'userinfo' not in request.session:
		if request.userinfo != None:
			request.session['userinfo'] = request.userinfo
	
	openid = request.session['openid']
	userinfo = request.session['userinfo']
	headimg = userinfo['headimgurl']
	nickname = userinfo['nickname']
	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 
	# 获取用户
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		# re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
		# filter_nickname = re_pattern.sub(u'\uFFFD', nickname) 
		# filter_account_name = re_pattern.sub(u'\uFFFD', account_name) 
		# print nickname,account_name,filter_nickname,filter_account_name 	
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account
		account_name = nickname + "的账户"
		print nickname,account_name
		account.name = account_name
		account.save()

	item_id = None
	if 'item_id' in request.GET:
		item_id = int(request.GET['item_id'])
	elif 'item_id' in request.POST:
		item_id = int(request.POST['item_id'])
	item = Item.objects.get(id=item_id)
	share_issue_result = {}
	share_issue_result['urllink'] = "http://2.juye51.com/shop/merchant_detail_info/?page_id=1&item_id=%d" % item_id
	if item.item_type.id == 2 and  item.proxy_sale_customer != None:
		share_issue_result['share_desc'] = "[%s发起一元夺宝活动] %s" % (customer.name,item.merchant.name)
		share_issue_result['share_title'] = "%s发起的一元夺宝" % customer.name
	else:
		share_issue_result['share_desc'] = "[一元夺宝活动] %s" % (item.merchant.name)
		share_issue_result['share_title'] = "一元夺宝活动"
	share_issue_result['share_imgpath'] = item.merchant.mer_img_oss_link
	return HttpResponse(json.dumps(share_issue_result))

################################################################
#
# 工具方法
#
################################################################


# 获取用户、账户信息
def fetch_customer_and_account(openid,nickname,headimg):
	# 获取用户
	customer = None
	account = None
	customers = Customer.objects.filter(openid=openid)
	if len(customers) == 0: # 不存在
		# 新建账户
		account_name = nickname + "的账户"
		account = Account.objects.create(name=account_name)
		account.save()
		customer = Customer.objects.create(account=account,name=nickname,nickname=nickname,openid=openid,headimg=headimg)
		customer.save()
	else:
		customer = customers[0]
		account = customer.account	
	return customer,account

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

def return_unicode_nickname(nickname):
	re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	nickname = re_pattern.sub(u'\uFFFD', nickname) 	
	return nickname
