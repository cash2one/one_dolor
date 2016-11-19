#coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
import xadmin
xadmin.autodiscover()

from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'juye_duobao.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$','weixin_message_handler.views.do'),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^xadmin/', include(xadmin.site.urls)),
    url(r'^duobao/admin/', include(xadmin.site.urls)),  	

    url(r'^test/','duobao_wechat_app.views.test'),
    url(r'^caonima/','duobao_wechat_app.views.caonima'),
    
    # 
    # 首页模块
    # 
    url(r'^index/','duobao_wechat_app.views.index'),
    # 
    # user模块
    # 
    # 个人页面
    url(r'^user/selfinfo/','duobao_wechat_app.views.selfinfo'),     # 个人主页
    url(r'^user/self_customer/','duobao_wechat_app.views.self_customer'), # 客服页面
    url(r'^user/win_record/','duobao_wechat_app.views.win_record'),    
    url(r'^user/pay_coins/','duobao_wechat_app.views.pay_coins'), # 用户充值
    url(r'^user/imporve_personal_info/','duobao_wechat_app.views.imporve_personal_info'), # 完善个人信息页
    url(r'^user/my_redpack/','duobao_wechat_app.views.my_redpack'), # 我的红包页
    url(r'^user/my_message/','duobao_wechat_app.views.my_message'), # 我的消息
    url(r'^user/recieve_address/','duobao_wechat_app.views.recieve_address'), # 地址管理
    url(r'^user/add_new_address/','duobao_wechat_app.views.add_new_address'), # 添加新地址
    url(r'^user/set_default_address/','duobao_wechat_app.views.set_default_address'),
    url(r'^user/delete_address/','duobao_wechat_app.views.delete_address'), # 删除地址    
    url(r'^user/my_invest_page/','duobao_wechat_app.views.my_invest_page'), # 邀请好友

    # 代卖
    url(r'^user/submit_proxy_selling_request/','duobao_wechat_app.views.submit_proxy_selling_request'), # 代卖请求
    url(r'^user/selling_merchant_request/','duobao_wechat_app.views.selling_merchant_request'), # 首次代卖请求
    url(r'^user/selling_merchant_detail_info/','duobao_wechat_app.views.selling_merchant_detail_info'), # 代卖详情页面（二维码、链接地址等）

    # 用户支付
    url(r'^user/submit_pay_request/','duobao_wechat_app.views.submit_pay_request'), # 用户提交支付请求    
    url(r'^user/wechat_pay_success/','duobao_wechat_app.views.wechat_pay_success'), # 用户提交支付请求    
    url(r'^user/submit_order_page/','duobao_wechat_app.views.submit_order_page'), # 用户提交支付请求    
    url(r'^user/submit_order_result/','duobao_wechat_app.views.submit_order_result'), # 用户提交支付返回结果
    url(r'^user/choose_submit_order_type/','duobao_wechat_app.views.choose_submit_order_type'), # 更换支付方式
    
    url(r'^user/order_wechat_payment_submit/','duobao_wechat_app.views.order_wechat_payment_submit'),
    url(r'^user/submit_wechat_order_pay/','duobao_wechat_app.views.submit_wechat_order_pay'),  # 订单中使用微信支付
    url(r'^user/wechat_tester_req/','duobao_wechat_app.views.wechat_tester_req'),
    
    # 支付回调
    url(r'user/wechat_recharge_payback','duobao_wechat_app.views.wechat_recharge_payback'),
    url(r'user/order_wechat_pay_notify_payback','duobao_wechat_app.views.order_wechat_pay_notify_payback'),
    url(r'user/test_payback','duobao_wechat_app.views.test_payback'),
    
    # 跳转页面
    url(r'^user/pay_success_jumper/','duobao_wechat_app.views.pay_success_jumper'),
    url(r'^user/recharge_success_jumper/','duobao_wechat_app.views.recharge_success_jumper'),
    url(r'^user/order_wait_wechat_pay_result/','duobao_wechat_app.views.order_wait_wechat_pay_result'),
    url(r'^user/order_wechat_pay_result_jumper/','duobao_wechat_app.views.order_wechat_pay_result_jumper'),

    # 提交表单
    url(r'^user/submit_address/','duobao_wechat_app.views.submit_address'),    # 提交新地址

    # url(r'^user/my_message/','duobao_wechat_app.views.my_message'),
    # 
    # Shop模块
    # 
    url(r'^shop/cart/','duobao_wechat_app.views.cart'),
    url(r'^shop/submit_cart_merchant/','duobao_wechat_app.views.submit_cart_merchant'),
    url(r'^shop/ten_yuan/','duobao_wechat_app.views.ten_yuan'),
    url(r'^shop/redpack_area/','duobao_wechat_app.views.redpack_area'), # 红包专区
    url(r'^shop/my_selling_list/','duobao_wechat_app.views.my_selling_list'),
    url(r'^shop/add_cart/','duobao_wechat_app.views.add_cart'), # ajax请求，添加购物车
    url(r'^shop/fetch_cart_json_data/','duobao_wechat_app.views.fetch_cart_json_data'), # ajax请求，获取购物车所有数据
    url(r'^shop/change_cart_list/','duobao_wechat_app.views.change_cart_list'),
    url(r'^shop/recent_announce/','duobao_wechat_app.views.recent_announce'), # 最新揭晓
    url(r'^shop/merchant_detail_info/','duobao_wechat_app.views.merchant_detail_info'), # 商品详情
    # 
    # 订单模块
    #     
    url(r'^record/my_all_records/','duobao_wechat_app.views.my_all_records'),
    url(r'^record/my_processing_records/','duobao_wechat_app.views.my_processing_records'),
    url(r'^record/my_over_records/','duobao_wechat_app.views.my_over_records'),
    url(r'^record/merchant_add_order/','duobao_wechat_app.views.merchant_add_order'),
    url(r'^record/winning_detail/','duobao_wechat_app.views.winning_detail'), # 中奖详情
    url(r'^record/my_item_tickets/','duobao_wechat_app.views.my_item_tickets'),
    url(r'^record/my_winning_records/','duobao_wechat_app.views.my_winning_records'), # 我的中奖记录
    url(r'^record/accept_reward/','duobao_wechat_app.views.accept_reward'),
    url(r'^record/calculate_winning_detail/','duobao_wechat_app.views.calculate_winning_detail'), # 计算中奖详情
    # 
    # 帮助模块
    #        
    url(r'^help/helpindex/','duobao_wechat_app.views.helpindex'),
    url(r'^help/liaojie_duobao/','duobao_wechat_app.views.liaojie_duobao'),
    url(r'^help/agreement/','duobao_wechat_app.views.agreement'),
    url(r'^help/common_question/','duobao_wechat_app.views.common_question'),
    url(r'^help/shop_delivery/','duobao_wechat_app.views.shop_delivery'),

    # 跑批
    url(r'batch/lottery_result_batch/','duobao_wechat_app.views.lottery_result_batch'),

    # jssdk方法
    url(r'jssdk/get_proxy_selling_jsapi_signature/','duobao_wechat_app.views.get_proxy_selling_jsapi_signature'),
    url(r'jssdk/get_merchant_detail_info_jsapi_signature/','duobao_wechat_app.views.get_merchant_detail_info_jsapi_signature'),
    url(r'jssdk/share_new_item/','duobao_wechat_app.views.share_new_item'),


    # 营销类游戏
    url(r'^game/draw_circle/','market_game_draw_circle.views.index'),
    url(r'^game/draw_circle/result/','market_game_draw_circle.views.result'),
    url(r'^game/draw_circle/resultpage/','market_game_draw_circle.views.resultpage'),
    url(r'^game/get_jsapi_signature/','market_game_draw_circle.views.get_jsapi_signature'),
    url(r'^game/share_game/','market_game_draw_circle.views.share_game'),

)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)   
