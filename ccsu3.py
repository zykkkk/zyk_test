# -*- coding:utf-8 -*-
_author_ = 'Administrator'

# ENGINE = lnnoDB DEFAULT CHARSET = UTF8
import pymysql
import re
import sys
import urllib.request
def createdatabase():
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='123456',charset='utf8',) #建立连接
    cursor=conn.cursor()                        #创建游标
    cursor.execute("create database if not exists web") #创建数据库
    cursor.execute("use web")
                                                #创建数据表
    cursor.execute(
        "create table if not exists ccsutest(id int not NULL AUTO_INCREMENT PRIMARY  KEY,name TINYTEXT NOT NULL ,address TINYTEXT NOT NULL,text TEXT NOT NULL)ENGINE = InnoDB DEFAULT CHARSET = UTF8")
    conn.commit()                               #提交，保存
    cursor.close()                              #关闭游标
    conn.close()                                #关闭连接
def gettext(web):
    response = urllib.request.urlopen(web)
    html = response.read()                      #获取网页代码
    html = html.decode('utf8')                  #解码
    r1 =r'<li><a href.*</span>'                 #网址正则表达式  r1
    r1 = re.compile(r1)                         #转换
    find = re.findall(r1, html)                 #寻找需要的信息
    return find
def get_news_text(web):							#获取新闻文本
    text=''
    response=urllib.request.urlopen(web)
    html=response.read()
    html=html.decode('utf8')
    html=html.replace('\n','')
    html=html.replace('&nbsp;','')
    html=html.replace('，','replace1')			#替换字符
    html=html.replace('、','replace2')
    html=html.replace('。','replace3')
    html=html.replace('；','replace4')
    html=html.replace(' ','replace5')
    html=html.replace('：','replace6')
    r1=r'v_news_content">(.*)</div></div>'		#获取文本位置
    r1=re.compile(r1)
    find=re.findall(r1,html)
    if(len(find)==0):
		print('ERROR')
        return text
    for texts in find:
        r2=r'>(\w+)<'							#寻找文本正则表达式
        r2=re.compile(r2)
        findtext=re.findall(r2,texts)
        for j in findtext:
            j =j.replace('replace1', '，')		#还原文本
            j =j.replace('replace2', '、')
            j =j.replace('replace3', '。')
            j =j.replace('replace4', '；')
            j =j.replace('replace5', ' ')
            j =j.replace('replace6', '：')
            text=text+j							#记录文本信息
    return text
def push(text):
    pre='http://www.ccsu.cn/'
    b=r'href="(.*)"><img'                       #地址的正则表达式 b
    c=re.compile(b)                             #转换 c
    d = re.findall(c,text)                      #寻找地址并返回元组 d
    e=r'/>(.*)<span'                            #标题的正则表达式 e
    f=re.compile(e)                             #转换
    g=re.findall(f,text)                        #获取所有的标题  g
    if(len(g)!=1):                              #判断是否个数统一
        print('error')
        print ('d->len: %d',len(text))
        print('g->len: %d',len(g))
        return 0
    conn2 = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', charset='utf8')  # 建立连接
    cursor2 = conn2.cursor()                    # 创建游标  cursor2
    cursor2.execute("use web")                  # 执行MySQL语句
    for i in range(len(g)):
       address=pre+d[0]                         #加上头的正确地址
       text=get_news_text(address)				#调用函数获取文本
       print(address,)
       j=g[i-1]                                 #获取含有标题的文本
       # j=j.replace('&ldquo;','')                #替换无用信息,适用于前一个官网
       # j=j.replace('&rdquo;','')                #替换无用信息,适用于前一个官网
       # j = j.replace('&mdash;', '')             #替换无用信息,适用于前一个官网
       j=j.replace('</a>','')                   #替换无用信息
       print (j)                                #输出标题
       l=(j,address,text)                            #把变量存入l中
       cursor2.execute("insert into ccsutest(name,address,text) values('%s','%s','%s')" %l)  #输出到数据库
       conn2.commit()                           # 提交，保存
    num=cursor2.execute("select * from ccsutest")   #读取数据库信息，验证结果
    cursor2.close()                             # 关闭游标
    conn2.close()                               # 关闭连接
    # print ('success')                           #输出数据库信息
    # print (num)
web1='http://www.ccsu.cn/'                      # 存储网址
createdatabase()                                #创建数据库
for i in gettext(web1):                        #存入数据库
    push(i)