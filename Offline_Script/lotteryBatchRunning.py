# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取时时彩数据

from bs4 import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import re
import DB
import datetime,time


page_link = "http://kjh.cailele.com/kj_ssc.shtml"

# 连接数据库 
def Connent_Online_Mysql_By_DB(hostname,port,username,pwd,dbname,socket):
    db = DB.DB(False,host=hostname, port=port, user=username ,passwd=pwd, db=dbname,charset='gbk', unix_socket=socket) 
    return db

# 写入数据库
def write_record_db(db,list_obj,table_name):
    try:
        db.insert(table_name,list_obj)
        db.commit()
    except Exception,e:
        print e

def update_record_db(db,list_obj,cond_obj,table_name):
    try:
        db.update(table_name,list_obj,cond_obj)
        db.commit()
    except Exception,e:
        print e

# 计算开奖结果
def cal_winning_result(db,lastest_issue_no,lastest_result):
	# 获取等待开奖的item
	waiting_lottery_items = db.select("select * from yiyuanduobao_shop_item where item_status_id = 4")

	for waiting_lottery_item in waiting_lottery_items:
		item_id = int(waiting_lottery_item[0]) 
		merchant_id = int(waiting_lottery_item[4])
		# 获取商品信息
		merchant_info = db.select('select * from yiyuanduobao_shop_merchant where id = %d' % merchant_id)
		merchant_price =  int(merchant_info[0][8])

		# 获取项目对应的所有奖券
		lottery_tickets = db.select("select * from yiyuanduobao_shop_lotteryticket where item_id = %d" % item_id)
		# 取末尾50条数据
		lottery_tickets = lottery_tickets[-50:]
		# print lottery_tickets
		total_sum = 0
		for lottery_ticket in lottery_tickets:
			ticket_createtime = lottery_ticket[2]
			ticket_createtime_str = ticket_createtime.strftime("%H%M%S")
			ticket_createtime_int = int(ticket_createtime_str)
			total_sum += ticket_createtime_int
		total_sum += int(lastest_result)
		winning_ticket = 100000000 + total_sum % merchant_price
		# 记录winning_ticket
		cond_dict = {}
		cond_dict['id'] = item_id
		result_dict= {}
		result_dict['winner_code'] = winning_ticket
		update_record_db(db,result_dict,cond_dict,"yiyuanduobao_shop_item")
		# 修改item状态
		item_status_result_dict = {}
		item_status_result_dict['item_status_id'] = 2
		update_record_db(db,item_status_result_dict,cond_dict,"yiyuanduobao_shop_item")
		print "result = ", winning_ticket
	# print waiting_lottery_items
	

# 获取时时彩数据
def fetch_lottery_data(db):
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
	lottery_db_select_result =  db.select("select * from yiyuanduobao_shop_lotteryresult where issue_no = %s and result = %s" % (lastest_issue_no,lastest_result))
	print lastest_issue_no,lastest_result
	if len(lottery_db_select_result) == 0:
		# 新开奖
		record = {}
		record["issue_no"] = lastest_issue_no
		record["result"] = lastest_result
		# 离线跑批兑奖
		cal_winning_result(db,lastest_issue_no,lastest_result)
		write_record_db(db,record,'yiyuanduobao_shop_lotteryresult')
	else:
		print "record exist!!"		
	

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','juye_duobao','/tmp/mysql.sock')	
	fetch_lottery_data(db)