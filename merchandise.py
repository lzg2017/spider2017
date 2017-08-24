# -*- coding: utf-8 -*-
"""
Created on Tue Aug 08 13:56:18 2017

@author: Administrator
"""
from pyquery import PyQuery as pq

import pandas as pd

from sqlalchemy import create_engine

import os

import glob

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#from itertools import izip_longest    # zip_longest -> Python 3, izip_longest -> Python 2  
#chunk_list = lambda a_list, n: izip_longest(*[iter(a_list)]*n)

class merchandise():
    
    def __init__(self):
        self.engine=create_engine('mysql://root:lzg000@127.0.0.1/stocksystem?charset=utf8')   
        self.csvdir=u'E:/股票数据/商品数据/'
        #self.rooturl='http://top.100ppi.com/'
    
    def periodUrl(self,findname,hyhtml,period):
        
        tmphtml=hyhtml[hyhtml.find(findname):]
        
        if period == '日':        
            tmphtml=tmphtml[:tmphtml.find(unicode(period))]
            
        elif period == '周':
            tmphtml=tmphtml[tmphtml.find(u'日'):tmphtml.find(unicode(period))]
        
        elif period == '月':
            tmphtml=tmphtml[tmphtml.find(u'周'):tmphtml.find(unicode(period))]
            
        elif period == '季':
            tmphtml=tmphtml[tmphtml.find(u'月'):tmphtml.find(unicode(period))]        
            
        elif period == '年':
            tmphtml=tmphtml[tmphtml.find(u'季'):tmphtml.find(unicode(period))]            
        
        findurl=pq(tmphtml)('a').attr.href
        
        return findurl


    def table(self,nydoc):
    
        textdoc=nydoc('table')('tr')
        
        tmplist=[]
        
        for i in textdoc:       
            
            tmptext=textdoc(i).text().split()      
            
            if len(tmptext)!=7:
                
                tmpdoc=textdoc(i)('td')
                
                tmptext=[]
                
                for j in tmpdoc:
                    
                    tmpchar=tmpdoc(j).text()
                    
                    if len(tmpchar)<=1:
                        
                        tmpchar=-1
                        
                    tmptext.append(tmpchar)          
                         
            tmplist.append(tmptext)
        
        #nylist = list(chunk_list(nytext.split(), 7))
        
        df_theday=pd.DataFrame(tmplist[1:],columns=['name','industry','close0','close','unit','chg','tbchg'])
               
        df_theday.drop(df_theday.columns[2],axis=1,inplace=True)
             
        return df_theday
    
    
    def download(self,name,period,days,update):
        
        name=unicode(name)
        
        if update == False:        
        
            fdir=os.path.join(self.csvdir,unicode(period))
                
            if not os.path.exists(fdir):
                os.mkdir(fdir)
                
            fname=os.path.join(fdir,name+'.csv')     
            
            if os.path.exists(fname):
                print fname
                flag=input(u'该文件已存在,是否要继续(1/0)')
                if flag != 1 :
                    return 0
                
        rooturl='http://top.100ppi.com/'
        
        doc=pq(rooturl)
        
        if name in ['期货近约榜','期货主约榜','农产品近约榜','工业品近约榜','有色金属近约榜','能源石化近约榜','农产品主约榜','工业品主约榜','有色金属主约榜','能源石化主约榜']:
        
            hydoc=doc('div[class="fl"]').eq(4)
            
            hyhtml=hydoc.html()
            
            url='http://top.100ppi.com/'+self.periodUrl(name,hyhtml,period).strip()   
            
            headurl=url[:url.find('fdetail')]
            
        
        elif name in ['稀土榜','化肥榜','氟化工榜','磷化工榜','溴化工榜','氯碱产业榜','甲醇产业榜','丙烯产业榜','苯乙烯产业榜','乙二醇产业榜','PTA产业榜','橡胶榜','塑料榜','资源商品榜','商品题材榜','五大钢材榜']:
            hydoc=doc('div[class="fl"]').eq(1)
        
            hyhtml=hydoc.html()
            
            url=self.periodUrl(name,hyhtml,period).strip()
        
            headurl=url[:url.find('detail')]
            
            table = 'boardday'
            
            nextclassid=1
            
        elif name in ['能源榜','化工榜','橡塑榜','纺织榜','有色榜','钢铁榜','建材榜','农副榜']:
            hydoc=doc('div[class="fl"]')
        
            hyhtml=hydoc.html()
            
            url=self.periodUrl(name,hyhtml,period).strip()
        
            headurl=url[:url.find('detail')]
            
            table = 'industryday' 
            
            nextclassid=2
            
                  
        doc=pq(url)
               
        df_days=pd.DataFrame()
        for i in xrange(days): 
                     
            df_theday=self.table(doc)
            
            title=doc('title').text()
            
            date=title[title.find('(')+1:title.find(')')].replace(u'年','-').replace(u'月','-').replace(u'日','')
            
            df_theday[u'date']=date
            
            if table == 'boardday':
                board=title[:title.find(u'价格')]             
                board=filter(lambda x:x not in '#0123456789',board)                
                df_theday['board']=board
            
            df_theday['chg']=(df_theday['chg'].str.replace('%','')).astype('float')
                        
            if update == False:
                if i==0:
                    df_theday.to_csv(fname,index=None,encoding='gbk')
                else:
                    df_theday.to_csv(fname,index=None,mode='a',encoding='gbk',header=None)            
            else:
                df_days=df_days.append(df_theday)               
                if i == (days-1):
                    df_days.drop_duplicates(inplace=True)
                    df_days.to_sql(table,con=self.engine,if_exists='append',index=None)
                            
            try:
                nynexturl=headurl+doc('div[class="phone"]').eq(nextclassid).find('a').attr.href
            except Exception as e:
                print e
                break
            
            doc=pq(nynexturl)
            
            print name+' '+date

    def industrySql(self,period):
        flist=glob.glob(u'E:\\股票数据\\商品数据\\'+period+'\\*.csv')
        for f in flist:
            s1=pd.read_csv(f,encoding='gbk')
            s1.columns=['name','industry','close','unit','chg','tbchg','date']
            s1['chg']=(s1['chg'].str.replace('%','')).astype('float')
            #s1.columns=['name','board','close','unit','chg','tbchg','date']
            s1.to_sql('industryday',con=self.engine,if_exists='append',index=None)
            
            print f   
            
    
    def boardSql(self,period):
        flist=glob.glob(u'E:\\股票数据\\商品数据\\'+period+'\\*.csv')
        for f in flist:
            s1=pd.read_csv(f,encoding='gbk')
            s1.columns=['name','industry','close','unit','chg','tbchg','date','board']
            s1['chg']=(s1['chg'].str.replace('%','')).astype('float')
            #s1.columns=['name','board','close','unit','chg','tbchg','date']
            s1.to_sql('boardday',con=self.engine,if_exists='append',index=None)
            
            print f          
        

if __name__ == '__main__':
    m=merchandise()
    qh=['期货近约榜','期货主约榜','农产品近约榜','工业品近约榜','有色金属近约榜','能源石化近约榜','农产品主约榜','工业品主约榜','有色金属主约榜','能源石化主约榜']
    ts=['稀土榜','化肥榜','氟化工榜','磷化工榜','溴化工榜','氯碱产业榜','甲醇产业榜','丙烯产业榜','苯乙烯产业榜','乙二醇产业榜','PTA产业榜','橡胶榜','塑料榜','资源商品榜','商品题材榜','五大钢材榜']
    hy=['能源榜','化工榜','橡塑榜','纺织榜','有色榜','钢铁榜','建材榜','农副榜']
    names=hy
    for name in names:
        m.download(name,'日',days=1,update=True)
    #m.boardSql('日')
