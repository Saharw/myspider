# -*- coding: utf-8 -*-
import json
import redis  # pip install redis
import pymysql

def main():
    # 指定redis数据库信息
    rediscli = redis.StrictRedis(host='192.168.110.128', port = 6379, db = 0)
    # 指定mysql数据库
    mysqlcli = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='mydb', charset='utf8',)

    # 无限循环
    while True:
        source, data = rediscli.blpop(["job_spider:items"]) # 从redis里提取数据

        item = json.loads(data.decode('utf-8')) # 把 json转字典

        try:
            # 使用cursor()方法获取操作游标
            cur = mysqlcli.cursor()
            # 使用execute方法执行SQL INSERT语句
            sql = 'insert into wuba_job(url,pname,smoney,emoney,location,syear,eyear,degree,person_num,ptype,time_pub,welfare,desc_job,company,crawl_time,webname) ' \
                  'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update time_pub=values(time_pub),smoney=VALUES(smoney),emoney=values(emoney)'
            cur.execute(sql, (item["url"], item["pname"], item["smoney"], item["emoney"], item["location"], item["syear"], item["eyear"],item["degree"], item["person_num"], item["ptype"], item["time_pub"], item["welfare"], item["desc_job"], item["company"], item["crawl_time"],item["webname"]))

            # 提交sql事务
            mysqlcli.commit()
            #关闭本次操作
            cur.close()
            print ("插入 %s" % item['pname'])
        except pymysql.Error as e:
            mysqlcli.rollback()
            print ("插入错误" ,str(e))

if __name__ == '__main__':
    main()