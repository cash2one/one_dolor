#coding:utf-8
'''
Created on 2014-5-13

@author: skycrab
'''

class WxPayConf_pub(object):
    """配置账号信息"""

    #=======【基本信息设置】=====================================
    #微信公众号身份的唯一标识。审核通过后，在微信发送的邮件中查看
    APPID = "wx3fa3ae3db5a07e8f"
    #JSAPI接口中获取openid，审核后在公众平台开启开发模式后可查看
    APPSECRET = "8204abe465a9ad178e0a8ea96f96bde8"
    #接口配置token
    TOKEN = "juye_one_dolor"
    #受理商ID，身份标识
    MCHID = "1311591001"
    #商户支付密钥Key。审核通过后，在微信发送的邮件中查看
    KEY = "a374192c4de712650f9bebb84a29b8df"
   
    WEB_DOMAIN = "http://2.juye51.com"
    #=======【异步通知url设置】===================================
    #异步通知url，商户根据实际开发过程设定
    ORDER_WECHAT_PAY_NOTIFY_URL = "http://2.juye51.com/user/order_wechat_pay_notify_payback"
    RECHARGE_NOTIFY_URL = "http://2.juye51.com/user/wechat_recharge_payback"
    TEST_NOTIFY_URL = "http://2.juye51.com/user/test_payback"
    # 发送红包IP
    CLIENT_IP = "123.57.1.71"

    #=======【证书路径设置】=====================================
    #证书路径,注意应该填写绝对路径
    SSLCERT_PATH = "/home/cert/apiclient_cert.pem"
    SSLKEY_PATH = "/home/cert/apiclient_key.pem"
    ROOT_CACERT_PATH = "/home/cert/apiclient_cert.p12"
    CACERT_PASSWD = "1311591001"

    #=======【curl超时设置】===================================
    CURL_TIMEOUT = 300

    #=======【HTTP客户端设置】===================================
    HTTP_CLIENT = "CURL"  # ("URLLIB", "CURL", "REQUESTS")


