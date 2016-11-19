#coding=utf8
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
import json
appid = "wx3fa3ae3db5a07e8f"
appsecret="8204abe465a9ad178e0a8ea96f96bde8"
token="juye_one_dolor"

conf = WechatConf(
    token=token, 
    appid=appid, 
    appsecret=appsecret)
# print conf
# print conf.get_access_token()
wechat_instance = WechatBasic(conf)
print wechat_instance
menu = {
    'button':[
        {
            'name': '一元夺宝',
            'sub_button': [
                {
                    'type': 'view',
                    'name': '桔叶夺宝店',
                    'url': 'http://2.juye51.com/index/?shop_id=1'
                },
                {
                    'type': 'click',
                    'name': '免费开夺宝店',
                    'key': 'V1001_TODAY_DUOBAO_SHOP'
                }
            ]
        },    
        {
            'name': '更多项目',
            'sub_button': [
                {
                    'type': 'click',
                    'name': '更多加盟项目',
                    'key': 'V1001_GOOD'                   
                }
            ]
     
        }
    ]
}
print wechat_instance.create_menu(menu)