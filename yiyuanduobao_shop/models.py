#coding=utf-8
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User, UserManager  
import django.utils.timezone as timezone

# 店铺
class Shop(models.Model):
	name = models.CharField(max_length=255,default="",verbose_name="商店名称")
	contract_name = models.CharField(max_length=255,default="",verbose_name="联系人姓名")
	contract_mobile = models.CharField(max_length=255,default="",verbose_name="联系人电话")
	addr = models.CharField(max_length=255,default="",verbose_name="联系人地址")
	shop_img = models.ImageField(verbose_name=u'店铺展示图片',upload_to='imgs/',blank=True,null=True)
	cert_front = models.ImageField(verbose_name=u'联系人证件正面照片',upload_to='imgs/',blank=True,null=True)
	cert_back = models.ImageField(verbose_name=u'联系人证件饭面照片',upload_to='imgs/',blank=True,null=True)
	shop_img_oss_link = models.CharField(max_length=1000,verbose_name=u'店铺展示图片存储地址',blank=True,null=True)
	cert_front_link = models.CharField(max_length=1000,verbose_name=u'联系人证件正面照片存储地址',blank=True,null=True)
	cert_back_link = models.CharField(max_length=1000,verbose_name=u'联系人证件反面照片存储地址',blank=True,null=True)
	qrcode_link = models.CharField(max_length=1000,verbose_name=u'店铺二维码',blank=True,null=True)
	create_time = models.DateTimeField(auto_now=True)
	update_time = models.DateTimeField(default=timezone.now)
	class Meta:
		verbose_name = '一元夺宝商店'
		verbose_name_plural  = '一元夺宝商店'
		ordering = ['-create_time']	
	def __unicode__(self):
		return "ID " + str(self.id) + " " + self.name

# 店铺管理员
class ShopManager(User):
	shop = models.OneToOneField(Shop,related_name="shop_owner",blank=True,null=True,verbose_name="管理的店铺") # 对应店铺
	is_agent = models.BooleanField(default=False,verbose_name=u'是否为代理商') # 是否为代理商
	agent_name = models.CharField(max_length=255,default="",verbose_name="代理商名称",blank=True,null=True)
	agent_shops = models.ManyToManyField(Shop,blank=True,null=True,verbose_name="代理的店铺",related_name="agent_shops")
	create_time = models.DateTimeField(auto_now=True)
	update_time = models.DateTimeField(default=timezone.now)
	class Meta:
		verbose_name = '夺宝店管理员'
		verbose_name_plural  = '夺宝店管理员'
		ordering = ['-create_time']	
	def __unicode__(self):
		if self.shop:
			return self.shop.name + " 的管理员"	
		else:
			return "代理商 " + self.agent_name

# 店铺首页banner图
class ShopBanner(models.Model):
	banner_img = models.ImageField(verbose_name=u'首页banner图',upload_to='imgs/') # 商店banner图
	banner_oss_img_link = models.CharField(max_length=1000,verbose_name=u'banner图存储地址',blank=True,null=True) # banner图存储地址
	banner_link = models.CharField(max_length=1000,verbose_name=u'banner链接地址',blank=True,null=True,default="#") # banner链接地址
	shop = models.ForeignKey(Shop,verbose_name="所属商店") # 所属商店

	class Meta:
		verbose_name = '首页轮播图'
		verbose_name_plural  = '首页轮播图'

# 账户
class Account(models.Model):
	name = models.CharField(max_length=255,default="",verbose_name="账户名") # 账户名
	balance_coins = models.IntegerField(default=0,verbose_name="夺宝币余额") # 夺宝币余额
	points = models.IntegerField(default=0,verbose_name="夺宝积分") # 夺宝积分
	total_recharge = models.IntegerField(default=0,verbose_name="总充值金额") # 总充值金额
	balance_redpack = models.IntegerField(default=0,verbose_name="可领红包金额") # 可领红包金额
	withdraw_redpack = models.IntegerField(default=0,verbose_name="已领红包金额") # 已领红包金额
	create_time = models.DateTimeField(auto_now=True)
	update_time = models.DateTimeField(default=timezone.now)
	class Meta:
		verbose_name = '账户'
		verbose_name_plural  = '账户'
		ordering = ['-create_time']	

	def __unicode__(self):
		return self.name

# 用户
class Customer(models.Model):
	account = models.OneToOneField(Account,verbose_name="账户",blank=True,null=True) # 账户
	name = models.CharField(max_length=255,default="",blank=True,null=True,verbose_name="用户名")
	mobile = models.CharField(max_length=255,default="",blank=True,null=True,verbose_name="手机号")
	headimg = models.CharField(max_length=255,default="",blank=True,null=True,verbose_name="头像")
	openid = models.CharField(max_length=255,default="",blank=True,null=True,verbose_name="微信openid")
	investor_id = models.IntegerField(default=-1,blank=True,null=True,verbose_name="推荐人的用户ID")
	nickname = models.CharField(max_length=255,default="",blank=True,null=True,verbose_name="昵称")
	password = models.CharField(max_length=255,default="",blank=True,null=True,verbose_name="密码")
	shops = models.ManyToManyField(Shop,blank=True,null=True,verbose_name="是哪些店的会员")
	create_time = models.DateTimeField(auto_now=True)
	update_time = models.DateTimeField(default=timezone.now)
	class Meta:
		verbose_name = '用户'
		verbose_name_plural  = '用户'
		ordering = ['-create_time']	

	def __unicode__(self):
		return self.name


# 消息状态 1-未读、2-已读、3-不显示（删除）
class NoticeMsgStatus(models.Model):
	status_name = models.CharField(max_length=255,default="",verbose_name="状态名称") # 状态名称

# 消息
class NoticeMsg(models.Model):
	customer = models.ForeignKey(Customer,verbose_name="所属用户",blank=True,null=True) # 所属用户
	shop = models.ForeignKey(Shop,verbose_name="所属商店",blank=True,null=True) # 所属商店
	title = models.CharField(max_length=255,default="",verbose_name="消息title") # 消息title
	context = models.CharField(max_length=3000,default="",verbose_name="消息内容") # 消息内容
	notice_msg_status = models.ForeignKey(NoticeMsgStatus,verbose_name="消息状态",blank=True,null=True) # 消息状态
	create_time = models.DateTimeField(default=timezone.now)
	update_time = models.DateTimeField(default=timezone.now,auto_now=True)

	class Meta:
		verbose_name = '消息'
		verbose_name_plural  = '消息'


# 收货地址
class Address(models.Model):
	customer = models.ForeignKey(Customer,verbose_name="所属用户",blank=True,null=True) # 所属用户
	name = models.CharField(max_length=255,default="",verbose_name="收件人姓名") # 收件人姓名
	province = models.CharField(max_length=255,default="",verbose_name="省") # 省
	city = models.CharField(max_length=255,default="",verbose_name="市") # 市
	district = models.CharField(max_length=255,default="",verbose_name="区") # 区
	detail_address = models.CharField(max_length=255,default="",verbose_name="详细地址") # 详细地址
	postcode = models.CharField(max_length=255,default="",verbose_name="邮编") # 邮编
	mobile = models.CharField(max_length=255,default="",verbose_name="收件人手机") # 收件人手机
	is_default_addr = models.IntegerField(default=0,verbose_name=u'是否为默认地址') # 0-不是，1-是默认地址
	create_time = models.DateTimeField(default=timezone.now)
	update_time = models.DateTimeField(default=timezone.now,auto_now=True)
	
	class Meta:
		verbose_name = '收货地址'
		verbose_name_plural  = '收货地址'
		ordering = ['-create_time']	

	def __unicode__(self):
		return self.name

# 中国全部地址
class AddrInfo(models.Model):
	code = models.IntegerField(default=0,verbose_name="地址码") # 地址码
	addr = models.CharField(max_length=255,default="",verbose_name="地址") # 地址


# 商品类型
class MerchantType(models.Model):
	name = models.CharField(max_length=255,default="",verbose_name="商品类型名称")
	def __unicode__(self):
		return self.name

# 商品
class Merchant(models.Model):
	name = models.CharField(max_length=255,default="",verbose_name=u'商品名称')
	shop = models.ForeignKey(Shop,related_name="shop_merchant",verbose_name="所属商店") # 对应的店铺
	mer_type = models.ForeignKey(MerchantType,verbose_name=u'商品类型') # 1-1元专区、2-红包专区、3-10元专区
	mer_img = models.ImageField(verbose_name=u'商品图片(330*330)',upload_to='imgs/') # 商品图片
	mer_thume_img = models.ImageField(verbose_name=u'商品缩略图图片(300*300)',upload_to='imgs/') # 商品缩略图图片
	mer_img_oss_link = models.CharField(verbose_name=u'商品图片地址',max_length=500,blank=True,null=True) # 商品图片oss地址
	mer_thume_img_oss_link = models.CharField(verbose_name=u'商品缩略图片地址',max_length=500,blank=True,null=True) # 商品缩略图片oss地址
	# banner_img = models.ManyToManyField(MerchantBannerImg,blank=True,null=True,verbose_name="轮播图片") # 轮播图片
	price = models.IntegerField(default=1,verbose_name=u'商品价格') 
	share = models.IntegerField(default=1,verbose_name=u'商品份数')
	commission_price = models.FloatField(default=0.0,verbose_name=u'代卖佣金') # 代卖佣金
	auto_up_shelve = models.BooleanField(default=True,verbose_name=u'本期结束，是否自动上架') # 是否自动上架
	create_time = models.DateTimeField(default=timezone.now)
	update_time = models.DateTimeField(default=timezone.now,auto_now=True)		
	class Meta:
		verbose_name = '商品'
		verbose_name_plural  = '商品'
		ordering = ['-create_time']
	def __unicode__(self):
		return self.name		

# 商品随机号码
class MerchantTicket(models.Model):
	ticket_index = models.IntegerField(default=0,verbose_name="下标") # 下标
	ticket_no = models.IntegerField(default=0,verbose_name="号码") # 号码

# 商品banner图片
class MerchantBannerImg(models.Model):
	name = models.CharField(max_length=255,default="",verbose_name="图片名称")
	img_link = models.ImageField(verbose_name=u'商品轮播图片',upload_to='imgs/') # 商品图片
	img_oss_link = models.CharField(verbose_name=u'商品轮播图链接',max_length=500,blank=True,null=True) # 轮播图oss地址
	create_time = models.DateTimeField(auto_now=True)
	update_time = models.DateTimeField(default=timezone.now)	
	merchant = models.ForeignKey(Merchant,blank=True,null=True,verbose_name="对应商品")
	shop = models.ForeignKey(Shop,blank=True,null=True,verbose_name="所属商店")
	class Meta:
		verbose_name = '商品轮播图片'
		verbose_name_plural  = '商品轮播图片'
		ordering = ['-create_time']

	def __unicode__(self):
		return self.name

# 商品某期状态
class ItemStatus(models.Model):
	name = models.CharField(max_length=255,default="",verbose_name=u'状态名称') # 1-进行中、2-已完成、3-已取消、4-等待开奖、5-用户已领奖，等待发货、6-商家已发货，本期结束
	def __unicode__(self):
		return self.name

# 项目类型（直营、代卖）
class ItemType(models.Model):
	name = models.CharField(max_length=255,default="",verbose_name=u'项目类型') # 1-直营、2-代卖

# 订单状态
class OrderStatus(models.Model):
	name = models.CharField(max_length=255,default="",verbose_name="状态名称")
	def __unicode__(self):
		return self.name



# 商品某期
class Item(models.Model):
	merchant = models.ForeignKey(Merchant,related_name="merchant_item",verbose_name="商品") # 对应的商品
	item_status = models.ForeignKey(ItemStatus,verbose_name="本期状态") # 1-进行中、2-已完成、3-已取消、4-等待开奖、5-用户已领奖，等待发货、6-商家已发货，本期结束
	take_part_num = models.IntegerField(default=0,verbose_name="已参与的价格") # 参与的价格（人次）
	item_code = models.CharField(max_length=255,default="",verbose_name=u'期号') # 本期期号
	winner_code = models.CharField(max_length=255,default="",verbose_name=u'中奖号码') # 中奖号码
	winner_lottery_result = models.CharField(max_length=255,default="",verbose_name=u'中奖对应时时彩号码') #中奖对应时时彩号码
	winner_customer = models.ForeignKey(Customer,verbose_name="中奖客户",blank=True,null=True,related_name='item_winner_customer') # 中奖客户
	# progress = models.FloatField(default=0.0,verbose_name="本期进度") # 本期进度
	item_type = models.ForeignKey(ItemType,verbose_name="项目类型",blank=True,null=True) # 1-直销、2-代卖
	proxy_sale_customer = models.ForeignKey(Customer,verbose_name="代销用户",blank=True,null=True) # 代销用户
	proxy_sale_qr_code = models.CharField(max_length=500,default="",verbose_name=u'本期代卖二维码') # 本期代卖二维码
	create_time = models.DateTimeField(default=timezone.now,verbose_name="本期开始时间")
	update_time = models.DateTimeField(auto_now=True,default=timezone.now)		
	lottery_time = models.DateTimeField(blank=True,null=True,verbose_name="本期中奖时间") # 本期中奖时间


	class Meta:
		verbose_name = '项目'
		verbose_name_plural  = '项目'
		ordering = ['-create_time']

	def __unicode__(self):
		return self.merchant.name + u" 第%08d期" % self.id

# 订单
class Order(models.Model):
	order_status = models.ForeignKey(OrderStatus,verbose_name=u'订单状态') # 1-进行中、2-已完成、3-已取消
	order_no = models.CharField(max_length=255,default="",verbose_name=u'订单号') # 订单号
	customer = models.ForeignKey(Customer,related_name="customer_order",verbose_name="参与用户") # 订单对应的用户
	item = models.ForeignKey(Item,related_name="item_order",verbose_name="参与项目") # 对应的期
	order_times = models.IntegerField(default=1,verbose_name=u'参与次数') # 本期参与次数（非人次）
	create_time = models.DateTimeField(default=timezone.now)
	update_time = models.DateTimeField(default=timezone.now,auto_now=True)	

	class Meta:
		verbose_name = '订单'
		verbose_name_plural  = '订单'
		ordering = ['-create_time']

	def __unicode__(self):
		return self.item.merchant.name + u" 第%8d期" % self.item.id + u"订单,订单ID为: %d " % self.id 

# 参与号码
class LotteryTicket(models.Model):
	item = models.ForeignKey(Item,verbose_name="对应项目",related_name="LotteryItem") # 对应项目
	order = models.ForeignKey(Order,verbose_name=u'对应订单',related_name="LotteryOrder")
	ticket_no = models.CharField(max_length=255,default="",verbose_name=u'参与号码') # 参与号码
	create_time = models.DateTimeField(default=timezone.now)
	update_time = models.DateTimeField(default=timezone.now,auto_now=True)	

	class Meta:
		verbose_name = '参与号码'
		verbose_name_plural  = '参与号码'
		ordering = ['-create_time']

	def __unicode__(self):
		return self.ticket_no



# 交易状态 # 1-待支付 2-已完成 3-已经失效 4-交易结束
class TransactionStatus(models.Model):
	transaction_desc = models.CharField(max_length=255,default="",verbose_name=u'状态说明') # 状态说明
	class Meta:
		verbose_name = '交易状态'
		verbose_name_plural  = '交易状态'

	def __unicode__(self):
		return self.transaction_desc	


# 交易方式 1- 余额支付 2-微信支付
class TransactionType(models.Model):
	transaction_type_desc = models.CharField(max_length=255,default="",verbose_name=u'交易方式') # 状态说明
	class Meta:
		verbose_name = '交易方式'
		verbose_name_plural  = '交易方式'

	def __unicode__(self):
		return self.transaction_type_desc	


# 交易
class Transaction(models.Model):
	customer = models.ForeignKey(Customer,verbose_name="交易用户",blank=True,null=True) 
	transaction_status = models.ForeignKey(TransactionStatus,verbose_name="交易状态",blank=True,null=True) # 1-待支付 2-已完成 3-已经失效 4-交易结束
	transaction_type = models.ForeignKey(TransactionType,verbose_name="交易方式",blank=True,null=True) # 1- 余额支付 2-微信支付
	orders = models.ManyToManyField(Order,blank=True,null=True,verbose_name="包含订单")
	transaction_no = models.IntegerField(default=1,verbose_name='交易编号')	
	create_time = models.DateTimeField(default=timezone.now)
	update_time = models.DateTimeField(default=timezone.now,auto_now=True)	
	class Meta:
		verbose_name = '交易'
		verbose_name_plural  = '交易'
		ordering = ['-create_time']
	def __unicode__(self):
		return self.transaction_no	

# 重庆老时时彩 中奖号码
class LotteryResult(models.Model):
	issue_no = models.CharField(max_length=255,default="",verbose_name=u'彩票期号') # 彩票期号
	result = models.CharField(max_length=255,default="",verbose_name=u'开奖结果') # 开奖结果
	create_time = models.DateTimeField(default=timezone.now)
	update_time = models.DateTimeField(default=timezone.now,auto_now=True)	
	class Meta:
		verbose_name = '时时彩'
		verbose_name_plural  = '时时彩'

	def __unicode__(self):
		return self.issue_no	