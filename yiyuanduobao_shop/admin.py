#coding=utf-8
from django.contrib import admin
from .models import *
import xadmin
from xadmin import views
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from django.contrib.auth.models import User, UserManager  
from xadmin.plugins.batch import BatchChangeAction
from weixin import WeixinHelper, JsApi_pub, WxPayConf_pub, UnifiedOrder_pub,Redpack_pub, Notify_pub, catch
import oss2
import datetime
from django.conf import settings

oss_auth = oss2.Auth('ddUxN1r8uyFGAybR','xchVItqu5yQcjspVQRBmTaIEQOVtRW')
oss_service = oss2.Service(oss_auth,'oss-cn-beijing.aliyuncs.com')
oss_cname = "juye-yiyuanduobao.oss-cn-beijing.aliyuncs.com"
class GlobalSetting(object):
    #设置base_site.html的Title
    site_title = '桔叶夺宝后台管理'
    #设置base_site.html的Footer
    site_footer  = '桔叶夺宝后台管理'
    def get_site_menu(self):
    	return (
              {
                'title': '商户管理', 
                'perm': self.get_model_perm(Shop, 'change'),
                'menus':(
                    {'title': '商店基本信息管理',  'url': self.get_model_url(Shop, 'changelist')},
                    {'title': '商店管理员管理',  'url': self.get_model_url(ShopManager, 'changelist')},                
                ),
              },                    
    		  # 客户管理
    		  {
    			'title': '客户管理', 
    			'perm': self.get_model_perm(Customer, 'view'),
    		    'menus':(
    		    	{'title': '客户信息管理',  'url': self.get_model_url(Customer, 'changelist')},
                    {'title': '账户管理',  'url': self.get_model_url(Account, 'changelist')},
                    {'title': '收货地址管理',  'url': self.get_model_url(Address, 'changelist')},

    			),
    		  },
              {
                'title': '商店管理', 
                'perm': self.get_model_perm(ShopBanner, 'view'),
                'menus':(
                    {'title': '商店轮播图管理',  'url': self.get_model_url(ShopBanner, 'changelist')},

                ),
              },                
              {
                'title': '商品管理', 
                'perm': self.get_model_perm(Merchant, 'view'),
                'menus':(
                    {'title': '商品管理',  'url': self.get_model_url(Merchant, 'changelist')},
                    {'title': '商品轮播图片管理',  'url': self.get_model_url(MerchantBannerImg, 'changelist')},
                    {'title': '项目（商品某期）管理',  'url': self.get_model_url(Item, 'changelist')},

                ),
              },  
              {
                'title': '订单管理', 
                'perm': self.get_model_perm(Order, 'view'),
                'menus':(
                    {'title': '订单查看',  'url': self.get_model_url(Order, 'changelist')},
                    # {'title': '交易管理',  'url': self.get_model_url(Transaction, 'changelist')},
                ),
              },         
              {
                'title': '兑奖信息管理', 
                'perm': self.get_model_perm(LotteryTicket, 'view'),
                'menus':(
                    {'title': '兑奖号码管理',  'url': self.get_model_url(LotteryTicket, 'changelist')},    
                    
                ),
              },                                  
    		)
    		
# 定制客户管理端信息
class CustomAdmin(object):
    refresh_times = (10, 30) # 
    def headimgPreview(self,obj):
        return '<img src="%s" height="80" width="100" />' %(obj.headimg)
    headimgPreview.allow_tags = True
    headimgPreview.short_description = "用户头像"

    def customer_address(self,obj):
        return Address.objects.get(customer_id=obj.id)

    # 本店信息过滤
    def get_list_queryset(self):
        if not self.user.is_superuser:
            current_shop_id = ShopManager.objects.get(user_ptr_id=self.user.id).shop_id
            current_shop = Shop.objects.get(id=current_shop_id)
            customers = current_shop.customer_set.all()
            results = super(CustomAdmin,self).get_list_queryset().filter(id=0) # 创建一个空的query_set
            for customer in customers:
                results = results | super(CustomAdmin,self).get_list_queryset().filter(id=customer.id)
            return results
        else:
            return super(CustomAdmin,self).get_list_queryset()

    customer_address.allow_tags = True
    customer_address.short_description = "用户收件地址"
    show_detail_fields = ['account']
    list_editable = ['account']
    list_display = ('name','mobile','account','headimgPreview')

# 定制商品管理端信息
class MerchantAdmin(object):
    def MerchantPreview(self,obj):
        return '<img src="%s" height="80" width="100" />' %(obj.mer_img_oss_link)
    MerchantPreview.allow_tags = True
    MerchantPreview.short_description = "商品图片"    

    def MerchantThumbPreview(self,obj):
        return '<img src="%s" height="80" width="100" />' %(obj.mer_thume_img_oss_link)
    MerchantThumbPreview.allow_tags = True
    MerchantThumbPreview.short_description = "商品缩略图片"  

    # 信息过滤
    def get_list_queryset(self):
        # 判断是否为超级用户
        if self.user.is_superuser:
            return super(MerchantAdmin,self).get_list_queryset()
        else:
            shop_manager = ShopManager.objects.get(user_ptr_id=self.user.id)
            current_shop_id = shop_manager.shop_id
            if shop_manager.is_agent == True:
                agent_shops = shop_manager.agent_shops.all()
                results = super(MerchantAdmin,self).get_list_queryset().filter(shop_id=0)
                for agent_shop in agent_shops:
                    results = results | super(MerchantAdmin,self).get_list_queryset().filter(shop_id=agent_shop.id)
                return results
            else:
                return super(MerchantAdmin,self).get_list_queryset().filter(shop_id=current_shop_id)

    def get_model_form(self, **kwargs):
        form = super(MerchantAdmin, self).get_model_form(**kwargs)
        current_path = self.request.path
        current_merchant_id = None
        current_merchant = None
        try:
            current_merchant_id = int(filter(lambda x:x.isdigit(),current_path))
            current_merchant = Merchant.objects.get(id=current_merchant_id)
        except:
            current_merchant = None

        if not self.user.is_superuser:
            current_shop_id = ShopManager.objects.get(user_ptr_id=self.user.id).shop_id
            form.base_fields['mer_type'].queryset = MerchantType.objects.filter(id=1) | MerchantType.objects.filter(id=3) # 暂时将红包过滤
            shop_manager = ShopManager.objects.get(user_ptr_id=self.user.id)
            if shop_manager.is_agent == True:       # 如果是代理商
                agent_shops = shop_manager.agent_shops.all()
                agent_shop_results = Shop.objects.filter(id=0)
                for agent_shop in agent_shops:
                    agent_shop_results = agent_shop_results | Shop.objects.filter(id=agent_shop.id)
                if current_merchant == None: # 新建
                    form.base_fields['shop'].queryset = agent_shop_results
                else: # 更新
                    form.base_fields['shop'].queryset = Shop.objects.filter(id=current_merchant.shop.id)
            else:   # 如果是普通商户
                shop_manager = ShopManager.objects.get(user_ptr_id=self.user.id)
                current_shop = shop_manager.shop
                form.base_fields['shop'].queryset = Shop.objects.filter(id=current_shop.id)

        return form

    # 保存数据
    def save_models(self):
        merchant_obj = self.new_obj
        author_id = self.request.user.id
        # print merchant_obj.shop
        # merchant_obj.shop_id = ShopManager.objects.get(user_ptr_id=author_id).shop_id
        
        merchant_obj.save()
        if merchant_obj.mer_img_oss_link == None:
            current_time_prefix = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")[:-3]
            mer_img_name = merchant_obj.mer_img.name[merchant_obj.mer_img.name.rfind('/')+1:]
            full_mer_img_name = "merchant_" + current_time_prefix + '_' + mer_img_name
            imgpath = settings.MEDIA_ROOT + '/' + merchant_obj.mer_img.name
            bucket = oss2.Bucket(oss_auth, oss_cname, 'juye-yiyuanduobao', is_cname=True)
            bucket.put_object_from_file(full_mer_img_name, imgpath)
            merchant_obj.mer_img_oss_link = settings.OSS_PATH_PREFIX + full_mer_img_name
        if merchant_obj.mer_thume_img_oss_link == None:
            current_time_prefix = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")[:-3]
            mer_thume_img_name = merchant_obj.mer_thume_img.name[merchant_obj.mer_thume_img.name.rfind('/')+1:]
            full_mer_thume_img_name = "merchant_thumb_" + current_time_prefix + '_' + mer_thume_img_name
            imgpath = settings.MEDIA_ROOT + '/' + merchant_obj.mer_thume_img.name
            bucket = oss2.Bucket(oss_auth, oss_cname, 'juye-yiyuanduobao', is_cname=True)
            bucket.put_object_from_file(full_mer_thume_img_name, imgpath)
            merchant_obj.mer_thume_img_oss_link = settings.OSS_PATH_PREFIX + full_mer_thume_img_name            
        merchant_obj.save()


    fields = ('name','mer_type','mer_img','shop','mer_thume_img','price','commission_price','auto_up_shelve')
    # raw_id_fields = ('name',)
    list_display = ('name','shop','MerchantPreview','MerchantThumbPreview','mer_type','price','commission_price','auto_up_shelve')
    list_filter = ('name','price','shop')

# 商品类型管理
# class MerchantTypeAdmin(object):
#     list_display = ('name',) 

# 商品轮播图片管理
class MerchantBannerImgAdmin(object):
    def ImgPreview(self,obj):
        return '<img src="%s" height="80" width="100" />' %(obj.img_oss_link)
    ImgPreview.allow_tags = True
    ImgPreview.short_description = "轮播图片"         
    # 信息过滤
    def get_list_queryset(self):
        # 判断是否为超级用户
        shop_manager = ShopManager.objects.get(user_ptr_id=self.user.id)
        if self.user.is_superuser:
            return super(MerchantBannerImgAdmin,self).get_list_queryset()
        else:
            current_shop_id = ShopManager.objects.get(user_ptr_id=self.user.id).shop_id
            if shop_manager.is_agent == True:       # 如果是代理商
                agent_shops = shop_manager.agent_shops.all()
                agent_merchant_banner_queryset_results = super(MerchantBannerImgAdmin,self).get_list_queryset().filter(id=0)
                for agent_shop in agent_shops:
                    agent_merchant_banner_queryset_results = agent_merchant_banner_queryset_results | super(MerchantBannerImgAdmin,self).get_list_queryset().filter(merchant__shop_id=agent_shop.id)
                return agent_merchant_banner_queryset_results
            else:
                return super(MerchantBannerImgAdmin,self).get_list_queryset().filter(merchant__shop_id=current_shop_id)        


    def get_model_form(self, **kwargs):
        form = super(MerchantBannerImgAdmin, self).get_model_form(**kwargs)
        current_shop_id = ShopManager.objects.get(user_ptr_id=self.user.id).shop_id
        current_path = self.request.path
        current_merchant_banner_id = None
        current_merchant_banner = None
        try:
            current_merchant_banner_id = int(filter(lambda x:x.isdigit(),current_path))
            current_merchant_banner = MerchantBannerImg.objects.get(id=current_merchant_banner_id)
        except:
            current_merchant_banner = None      

        if not self.user.is_superuser:
            shop_manager = ShopManager.objects.get(user_ptr_id=self.user.id)
            if shop_manager.is_agent == True:       # 如果是代理商
                agent_shops = shop_manager.agent_shops.all()
                agent_shop_results = Shop.objects.filter(id=0)
                agent_merchant_results = Merchant.objects.filter(id=0)
                for agent_shop in agent_shops:
                    agent_shop_results = agent_shop_results | Shop.objects.filter(id=agent_shop.id)  
                    agent_merchant_results = agent_merchant_results | Merchant.objects.filter(shop_id=agent_shop.id)              
                if current_merchant_banner == None: # 新建
                    # form.base_fields['shop'].queryset = agent_shop_results
                    form.base_fields['merchant'].queryset = agent_merchant_results
                else: # 更新
                    form.base_fields['merchant'].queryset = Merchant.objects.filter(id=current_merchant_banner.merchant.id)
                    # form.base_fields['shop'].queryset = Shop.objects.filter(id=current_merchant_banner.shop.id)  
            else:   # 如果是普通商户   
                form.base_fields['merchant'].queryset = Merchant.objects.filter(shop_id=current_shop_id)
                # form.base_fields['shop'].queryset = Shop.objects.filter(id=current_shop_id)
        return form

    # 保存数据
    def save_models(self):
        merchant_banner_obj = self.new_obj
        merchant_banner_obj.shop = merchant_banner_obj.merchant.shop
        merchant_banner_obj.save()
        if merchant_banner_obj.img_oss_link == None:
            current_time_prefix = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")[:-3]
            img_link_name = merchant_banner_obj.img_link.name[merchant_banner_obj.img_link.name.rfind('/')+1:]
            full_img_link_name = "merchant_banner_" + current_time_prefix + '_' + img_link_name
            imgpath = settings.MEDIA_ROOT + '/' + merchant_banner_obj.img_link.name
            bucket = oss2.Bucket(oss_auth, oss_cname, 'juye-yiyuanduobao', is_cname=True)
            bucket.put_object_from_file(full_img_link_name, imgpath)
            merchant_banner_obj.img_oss_link = settings.OSS_PATH_PREFIX + full_img_link_name           
        merchant_banner_obj.save()

    fields =  ('name','img_link','merchant')  
    list_display = ('name','ImgPreview','merchant','shop')
    list_filter = ('name','merchant','shop')

# 定制商店信息
class ShopAdmin(object):

    # 店铺图片展示
    def ShopImgPreview(self,obj):
        return '<img src="%s" height="80" width="100" />' %(obj.shop_img_oss_link)
    ShopImgPreview.allow_tags = True
    ShopImgPreview.short_description = "店铺展示图片"   

    # 证件正面显示
    def CertFrontPreview(self,obj):
        return '<img src="%s" height="80" width="100" />' %(obj.cert_front_link)
    CertFrontPreview.allow_tags = True
    CertFrontPreview.short_description = "联系人证件正面"   

    # 证件反面显示
    def CertBackPreview(self,obj):
        return '<img src="%s" height="80" width="100" />' %(obj.cert_back_link)
    CertBackPreview.allow_tags = True
    CertBackPreview.short_description = "联系人证件反面" 

    # 店铺地址
    def ShopUrlLink(self,obj):
        return 'http://2.juye51.com/index/?shop_id=%d' %(obj.id)
    ShopUrlLink.allow_tags = True
    ShopUrlLink.short_description = "店铺生成地址(供微信用户使用)"         

    # 微信二维码地址
    def qrcodePreview(self,obj):
        shop_link = 'http://2.juye51.com/index/?shop_id=%d' %(obj.id)
        if obj.qrcode_link == None:
            obj.qrcode_link = "http://pan.baidu.com/share/qrcode?w=280&h=280&url=%s" % shop_link
            obj.save()
        return '<img src="%s" height="80" width="100" />' %(obj.qrcode_link)
    qrcodePreview.allow_tags = True
    qrcodePreview.short_description = "店铺二维码显示"   
    # 信息过滤
    def get_list_queryset(self):
        # 判断是否为超级用户
        if self.user.is_superuser:
            return super(ShopAdmin,self).get_list_queryset()
        else:
            shop_manager = ShopManager.objects.get(user_ptr_id=self.user.id)
            current_shop_id = shop_manager.shop_id
            results = None
            if shop_manager.is_agent == True:       # 如果是代理商
                agent_shops = shop_manager.agent_shops.all() 
                results = super(ShopAdmin,self).get_list_queryset().filter(id=0)        
                for agent_shop in agent_shops:
                    results = results | super(ShopAdmin,self).get_list_queryset().filter(id=agent_shop.id)     
                return results
            else:
                results = super(ShopAdmin,self).get_list_queryset().filter(id=current_shop_id)
            return results    
    # 保存对象，默认变为自己的代理商铺
    def save_models(self):
        shop_obj = self.new_obj
        
        # 获取当前登录用户
        shop_manager = None
        try:
            shop_manager = ShopManager.objects.get(user_ptr_id=self.user.id)
        except:
            shop_manager = None

        # current_shop_id = shop_manager.shop_id
        shop_obj.save()

        # 店铺展示图片
        if shop_obj.shop_img != None:
            current_time_prefix = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")[:-3]
            img_link_name = shop_obj.shop_img.name[shop_obj.shop_img.name.rfind('/')+1:]
            full_img_link_name = "shop_cert_front_" + current_time_prefix + '_' + img_link_name
            imgpath = settings.MEDIA_ROOT + '/' + shop_obj.shop_img.name
            bucket = oss2.Bucket(oss_auth, oss_cname, 'juye-yiyuanduobao', is_cname=True)
            bucket.put_object_from_file(full_img_link_name, imgpath)
            shop_obj.shop_img_oss_link = settings.OSS_PATH_PREFIX + full_img_link_name   

        # 证件正面图片
        if shop_obj.cert_front != None:
            current_time_prefix = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")[:-3]
            img_link_name = shop_obj.cert_front.name[shop_obj.cert_front.name.rfind('/')+1:]
            full_img_link_name = "shop_cert_front_" + current_time_prefix + '_' + img_link_name
            imgpath = settings.MEDIA_ROOT + '/' + shop_obj.cert_front.name
            bucket = oss2.Bucket(oss_auth, oss_cname, 'juye-yiyuanduobao', is_cname=True)
            bucket.put_object_from_file(full_img_link_name, imgpath)
            shop_obj.cert_front_link = settings.OSS_PATH_PREFIX + full_img_link_name        

        # 证件反面图片
        if shop_obj.cert_back != None:
            current_time_prefix = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")[:-3]
            img_link_name = shop_obj.cert_back.name[shop_obj.cert_back.name.rfind('/')+1:]
            full_img_link_name = "shop_cert_front_" + current_time_prefix + '_' + img_link_name
            imgpath = settings.MEDIA_ROOT + '/' + shop_obj.cert_back.name
            bucket = oss2.Bucket(oss_auth, oss_cname, 'juye-yiyuanduobao', is_cname=True)
            bucket.put_object_from_file(full_img_link_name, imgpath)
            shop_obj.cert_back_link = settings.OSS_PATH_PREFIX + full_img_link_name   

        shop_obj.save()
        if shop_manager and shop_manager.is_agent == True:       # 如果是代理商
            shop_manager.agent_shops.add(shop_obj)
            shop_manager.save()

    fields = ('name','contract_name','contract_mobile','addr','shop_img','cert_front','cert_back')
    list_display = ('name','contract_name','contract_mobile','addr','ShopImgPreview','CertFrontPreview','CertBackPreview','ShopUrlLink','qrcodePreview')
    search_fields = ('name',)
    # 查询过滤
    # def get_list_queryset(self):
    #     print "current user id = ", self.user.id
    #     # 判断是否为超级用户
    #     if not self.user.is_superuser:
    #         # 获取shop id
    #         current_shop_id = ShopManager.objects.get(user_ptr_id=self.user.id).shop_id
    #         return super(SubdishAdmin,self).get_list_queryset().filter(shop_id=current_shop_id)
    #     else:
    #         return super(SubdishAdmin,self).get_list_queryset()    

# 定制商店管理员信息
class ShopManagerAdmin(object):
    def save_models(self):
        self.new_obj.save()
        current_user_id = self.new_obj.user_ptr_id
        current_shop_id = self.new_obj.shop_id
        current_obj = self.new_obj
        current_user = User.objects.get(id=current_user_id)
        current_user.set_password(self.new_obj.password)
        # print current_user.password
        current_obj.password = current_user.password
        current_obj.save()
    
    # queryset filter
    def get_list_queryset(self):
        if not self.user.is_superuser:
            shop_manager = ShopManager.objects.get(user_ptr_id=self.user.id)
            current_shop_id = shop_manager.shop_id
            results = None            
            if shop_manager.is_agent == True:       # 如果是代理商
                agent_shops = shop_manager.agent_shops.all() 
                results = super(ShopManagerAdmin,self).get_list_queryset().filter(shop_id=0)        
                for agent_shop in agent_shops:
                    results = results | super(ShopManagerAdmin,self).get_list_queryset().filter(shop_id=agent_shop.id)      
                return results          
            else:            
              return super(ShopManagerAdmin,self).get_list_queryset().filter(shop_id=current_shop_id)
        else:
            return super(ShopManagerAdmin,self).get_list_queryset()
    # fields = ('shop','user')


# 定制商店某期信息
class ItemAdmin(object):

    # 所属商店显示
    def item_shop(self,obj):
        shop = obj.merchant.shop
        return shop
    item_shop.allow_tags = True
    item_shop.short_description = "所属商店"
    
    # 进度显示
    def progressView(self,obj):
        # orders = Order.objects.filter(item_id=obj.id).exclude(order_status_id=3)
        progress = float(obj.take_part_num) / float(obj.merchant.price)        
        return "%.1f" % (progress*100.0) + "%"
    progressView.allow_tags = True
    progressView.short_description = "本期进度"

    # 中奖人地址信息
    def winner_customer_addr(self,obj):
        if obj.winner_customer == None:
            return '<span style="color:green"> 本期进行中 </span>'
        addrs = Address.objects.filter(customer=obj.winner_customer,is_default_addr=1)
        if len(addrs) == 0:
            return '<span style="color:red"> 用户尚未上传默认收货地址 </span>'
        else:
            addr = addrs[0]
            return '<span style="color:blue"> %s </span>' % (addr.province + ' ' + addr.city + ' ' + addr.district + '\n' + addr.detail_address+ '\n' + '邮编:' + addr.postcode + '\n收货人电话:' + addr.mobile) 
    winner_customer_addr.allow_tags = True
    winner_customer_addr.short_description = "本期中奖人收货地址"
    # 本期商品价格
    def merchant_price(self,obj):
        return obj.merchant.price
    merchant_price.allow_tags = True
    merchant_price.short_description = "本期总价格"

    # 本期类型（直销or代卖）
    def current_item_type(self,obj):
        if obj.item_type_id == 1:
            return "直销"
        elif obj.item_type_id == 2:
            return '<span style="color:red"> %s 代卖 </span>' % obj.proxy_sale_customer.name
            # return "%s 代卖" % obj.proxy_sale_customer.name
        else:
            return "直销"
        # return "%08d" % obj.id
    current_item_type.allow_tags = True
    current_item_type.short_description = "本期类型（直销or代卖）"

    # 信息过滤
    def get_list_queryset(self):
        # 判断是否为超级用户
        if self.user.is_superuser:
            return super(ItemAdmin,self).get_list_queryset()
        else:
            shop_manager = ShopManager.objects.get(user_ptr_id=self.user.id)
            current_shop_id = shop_manager.shop_id
            if shop_manager.is_agent:
                agent_shops = shop_manager.agent_shops.all()
                results = super(ItemAdmin,self).get_list_queryset().filter(merchant__shop_id=0)
                for agent_shop in agent_shops:
                    results = results | super(ItemAdmin,self).get_list_queryset().filter(merchant__shop_id=agent_shop.id)
                return results
            else:
                return super(ItemAdmin,self).get_list_queryset().filter(merchant__shop_id=current_shop_id)        

    # def get_list_display(self):
    #     list_display = super(MyAdmin, self). get_list_display()
    #     if not self.user.is_superuser:
        
    #     return list_display

    # 过滤下拉框
    def get_model_form(self, **kwargs):
        form = super(ItemAdmin, self).get_model_form(**kwargs)
        current_path = self.request.path
        current_item_id = None
        current_item = None
        try:
            current_item_id = int(filter(lambda x:x.isdigit(),current_path))
            current_item = Item.objects.get(id=current_item_id)
        except:
            current_item = None
        if not self.user.is_superuser:
            current_shop_id = ShopManager.objects.get(user_ptr_id=self.user.id).shop_id
            print self.user.id
            if current_item == None: # 新建item
                shop_manager = ShopManager.objects.get(user_ptr_id=self.user.id)
                current_shop_id = shop_manager.shop_id
                print "!!!"
                if shop_manager.is_agent:
                    print "agent!"
                    agent_shops = shop_manager.agent_shops.all()
                    results = Merchant.objects.filter(id=0)
                    for agent_shop in agent_shops:
                        results = results | Merchant.objects.filter(shop__id=agent_shop.id)
                    form.base_fields['merchant'].queryset = results
                else:
                    form.base_fields['merchant'].queryset = Merchant.objects.filter(shop_id=current_shop_id)
                
                form.base_fields['item_status'].queryset = ItemStatus.objects.filter(id=1)
            else:
                shop_manager = ShopManager.objects.get(user_ptr_id=self.user.id)
                current_shop_id = shop_manager.shop_id
                if shop_manager.is_agent:
                    agent_shops = shop_manager.agent_shops.all()
                    results = Merchant.objects.filter(id=0)
                    for agent_shop in agent_shops:
                        results = results | Merchant.objects.filter(shop__id=agent_shop.id)
                else:
                    form.base_fields['merchant'].queryset = Merchant.objects.filter(id=current_item.merchant.id)
                current_item_status = current_item.item_status
                if current_item_status.id == 5:
                    form.base_fields['item_status'].queryset = ItemStatus.objects.filter(id=6)
                else:
                    form.base_fields['item_status'].queryset = ItemStatus.objects.filter(id=current_item_status.id)
        return form
    
    def save_models(self):
        item = self.new_obj
        if item.item_status_id == 1:
            item.item_status_id = 1
            item.save() 
            item.item_code = str(100000000 + int(item.id))
            item.item_type_id = 1 # 直销
            item.save()
        elif item.item_status_id == 6:
            item.save()
    fields = ('merchant','item_status')
    list_display = ('id','item_code',"item_shop",'merchant','item_status','current_item_type','merchant_price','take_part_num','winner_code','winner_customer','winner_customer_addr','progressView','proxy_sale_customer')
    list_filter = ('merchant','item_status','item_code','proxy_sale_customer')

# 定制订单管理
class OrderAdmin(object):
    # 商品期号
    def orderCode(self,obj):
        return "%08d" % obj.id
    orderCode.allow_tags = True
    orderCode.short_description = "本期订单号"    
    fields = ('item','order_times','customer','order_status')
    list_display = ('item','orderCode','order_times','customer','order_status')
    list_filter = ('item',)
   # queryset filter
    def get_list_queryset(self):
        if not self.user.is_superuser:
            shop_manager = ShopManager.objects.get(user_ptr_id=self.user.id)
            current_shop_id = shop_manager.shop_id
            if shop_manager.is_agent == True:
                agent_shops = shop_manager.agent_shops.all()
                results = super(OrderAdmin,self).get_list_queryset().filter(id=0)
                for agent_shop in agent_shops:
                    results = results | super(OrderAdmin,self).get_list_queryset().filter(item__merchant__shop_id__exact=agent_shop.id)
                return results   
            else:         
                return super(OrderAdmin,self).get_list_queryset().filter(item__merchant__shop_id__exact=current_shop_id)
        else:
            return super(OrderAdmin,self).get_list_queryset()

# 定制账户管理
class AccountAdmin(object):
    def participate_amount(self,obj):
        customer = Customer.objects.get(account_id=obj.id)
        # 获取orders
        orders = Order.objects.filter(customer=customer).exclude(order_status_id=3)
        invest_price = 0
        for order in orders:
            if order.item.merchant.mer_type_id == 3:
                invest_price += order.order_times * 10
            else:
                invest_price += order.order_times
        return invest_price
    participate_amount.allow_tags = True
    participate_amount.short_description = "已参与金额" 

    # 本店信息过滤
    def get_list_queryset(self):
        if not self.user.is_superuser:
            current_shop_id = ShopManager.objects.get(user_ptr_id=self.user.id).shop_id
            current_shop = Shop.objects.get(id=current_shop_id)
            customers = current_shop.customer_set.all()
            results = super(AccountAdmin,self).get_list_queryset().filter(id=0) # 创建一个空的query_set
            for customer in customers:
                results = results | super(AccountAdmin,self).get_list_queryset().filter(id=customer.account.id)
            return results
        else:
            return super(AccountAdmin,self).get_list_queryset()

    fields = ('name','balance_coins','points','total_recharge','balance_redpack','withdraw_redpack')
    list_display = ('name','balance_coins','points','total_recharge','balance_redpack','withdraw_redpack','participate_amount')

# 收货地址管理
class AddressAdmin(object):
    def previewAddrDefault(self,obj):
        if obj.is_default_addr == 1:
            return "是默认地址"
        else:
            return "不是默认地址"

    # 收货地址信息过滤
    def get_list_queryset(self):
        if not self.user.is_superuser:
            current_shop_id = ShopManager.objects.get(user_ptr_id=self.user.id).shop_id
            current_shop = Shop.objects.get(id=current_shop_id)
            customers = current_shop.customer_set.all()
            results = super(AddressAdmin,self).get_list_queryset().filter(id=0) # 创建一个空的query_set
            for customer in customers:
                results = results | super(AddressAdmin,self).get_list_queryset().filter(customer=customer)
            return results
        else:
            return super(AddressAdmin,self).get_list_queryset()            
    fields = ('customer','name','province','city','district','detail_address','postcode','mobile')
    list_display = ('customer','name','province','city','district','detail_address','postcode','mobile','previewAddrDefault')

# 交易管理
class TransactionAdmin(object):
    fields = ('customer','transaction_status','orders','transaction_no')
    list_display = ('customer','transaction_status','orders','transaction_no')

   # queryset filter
    def get_list_queryset(self):
        if not self.user.is_superuser:
            current_shop_id = ShopManager.objects.get(user_ptr_id=self.user.id).shop_id
            return super(OrderAdmin,self).get_list_queryset().filter(orders__item__merchant__shop_id__exact=current_shop_id)
        else:
            return super(OrderAdmin,self).get_list_queryset()

# 兑奖号码
class LotteryTicketAdmin(object):
    fields = ('item','order','ticket_no')
    list_display = ('item','order','ticket_no')
    list_filter = ('item','order','ticket_no')
   # queryset filter
    def get_list_queryset(self):
        if not self.user.is_superuser:
            current_shop_id = ShopManager.objects.get(user_ptr_id=self.user.id).shop_id
            return super(LotteryTicketAdmin,self).get_list_queryset().filter(item__merchant__shop_id__exact=current_shop_id)
        else:
            return super(LotteryTicketAdmin,self).get_list_queryset()

# 商户banner
class ShopBannerAdmin(object):
    def ImgPreview(self,obj):
        return '<img src="%s" height="80" width="100" />' %(obj.banner_oss_img_link)
    ImgPreview.allow_tags = True
    ImgPreview.short_description = "轮播图片(730*350)"        
        
    def get_model_form(self, **kwargs):
        form = super(ShopBannerAdmin, self).get_model_form(**kwargs)
        current_shop_id = ShopManager.objects.get(user_ptr_id=self.user.id).shop_id

        current_path = self.request.path
        current_shop_banner_id = None
        current_shop_banner = None

        try:
            current_shop_banner_id = int(filter(lambda x:x.isdigit(),current_path))
            current_shop_banner = Merchant.objects.get(id=current_shop_banner_id)
        except:
            current_shop_banner = None

        if not self.user.is_superuser:
            shop_manager = ShopManager.objects.get(user_ptr_id=self.user.id)
            if shop_manager.is_agent == True:       # 如果是代理商
                if current_shop_banner == None: # 新建
                    agent_shops = shop_manager.agent_shops.all()
                    agent_shop_results = Shop.objects.filter(id=0)
                    for agent_shop in agent_shops:
                        agent_shop_results = agent_shop_results | Shop.objects.filter(id=agent_shop.id)                
                    form.base_fields['shop'].queryset = agent_shop_results
                else:
                    form.base_fields['shop'].queryset = Shop.objects.filter(id=current_shop_banner.shop.id)
            else:
                form.base_fields['shop'].queryset = Shop.objects.filter(id=current_shop_id)
        return form    

    # 保存数据
    def save_models(self):
        shop_banner_obj = self.new_obj
        shop_banner_obj.save()
        if shop_banner_obj.banner_oss_img_link == None:
            current_time_prefix = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")[:-3]
            img_link_name = shop_banner_obj.banner_img.name[shop_banner_obj.banner_img.name.rfind('/')+1:]
            full_img_link_name = "shop_banner_" + current_time_prefix + '_' + img_link_name
            imgpath = settings.MEDIA_ROOT + '/' + shop_banner_obj.banner_img.name
            bucket = oss2.Bucket(oss_auth, oss_cname, 'juye-yiyuanduobao', is_cname=True)
            bucket.put_object_from_file(full_img_link_name, imgpath)
            shop_banner_obj.banner_oss_img_link = settings.OSS_PATH_PREFIX + full_img_link_name           
        shop_banner_obj.save()        
    fields = ('banner_img','shop')
    list_display = ('ImgPreview','shop') 

    def get_list_queryset(self):
        if not self.user.is_superuser:
            shop_manager = ShopManager.objects.get(user_ptr_id=self.user.id)
            current_shop_id = shop_manager.shop_id
            results = None            
            if shop_manager.is_agent == True:       # 如果是代理商
                print 'a'
                agent_shops = shop_manager.agent_shops.all() 
                results = super(ShopBannerAdmin,self).get_list_queryset().filter(shop__id=0)        
                for agent_shop in agent_shops:
                    results = results | super(ShopBannerAdmin,self).get_list_queryset().filter(shop__id=agent_shop.id)      
                return results          
            else:            
              return super(ShopBannerAdmin,self).get_list_queryset().filter(shop__id=current_shop_id)
        else:
            return super(ShopBannerAdmin,self).get_list_queryset()
  

# 自定义方法
# 获取wechat的client
def fetch_wechatpy_client():
    appid = WxPayConf_pub.APPID
    appsecret = WxPayConf_pub.APPSECRET
    client = WeChatClient(appid, appsecret)
    return client

xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(Customer,CustomAdmin)
xadmin.site.register(Merchant,MerchantAdmin)
xadmin.site.register(MerchantBannerImg,MerchantBannerImgAdmin)
xadmin.site.register(Shop,ShopAdmin)
xadmin.site.register(ShopManager,ShopManagerAdmin)
xadmin.site.register(Item,ItemAdmin)
xadmin.site.register(Order,OrderAdmin)
xadmin.site.register(Account,AccountAdmin)
xadmin.site.register(Address,AddressAdmin)
xadmin.site.register(ShopBanner,ShopBannerAdmin)
# xadmin.site.register(Transaction,TransactionAdmin)
xadmin.site.register(LotteryTicket,LotteryTicketAdmin)