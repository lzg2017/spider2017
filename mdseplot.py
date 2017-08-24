#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-08-15 09:51:24
# Project: s8

import xlsxwriter

from sqlalchemy import create_engine 

import pandas as pd

import os

class mdsePlot:
    
    def __init__(self,sdate,edate):
        
        self.engine=create_engine('mysql://root:lzg000@127.0.0.1/stocksystem?charset=utf8')
        
        self.fdir=(u'E:\\工作\\报表\\商品\\') 
                
        self.sdate=sdate        
        
        self.edate=edate
        

    #得到关联上下游股票名称的series
    def relatedStock(self,merchandise,streamdata):
        #streamdata=pd.read_sql('select * from industryday where date >=  "'+sdate+'" and date <= "'+edate+'"')
        relatedup=streamdata[streamdata.name==merchandise]['up']
        
        relateddown=streamdata[streamdata.name==merchandise]['down']
            
        return relatedup,relateddown
    

    def plot(self,scope): 
        #生成4个商品为一组的图
        def addChartSet(loopindex,width,height):
         
           data_top=1
           
           interval=linewidth+1
           
           loopinterval=4*interval
           
           bk_chart = wbk.add_chart({'type': 'line'})   
              
           bk_chart.set_style(4)
           #向图表添加数据 
               #沪深300
           bk_chart.add_series({
            'name':['data', 1, namecol+loopindex*loopinterval],
            'categories':['data', data_top, datecol+loopindex*loopinterval, data_top+maxlen, datecol+loopindex*loopinterval],
            'values':['data', data_top, chgcol+loopindex*loopinterval, data_top+maxlen,chgcol+loopindex*loopinterval],
            'line':{'color':'FF0033'},#FF6666
            })
        
                #所选数据1
           bk_chart.add_series({
            'name':['data', 1, namecol+interval+loopindex*loopinterval],
            'categories':['data', data_top, datecol+interval+loopindex*loopinterval, data_top+maxlen, datecol+interval+loopindex*loopinterval],
            'values':['data', data_top, chgcol+interval+loopindex*loopinterval, data_top+maxlen,chgcol+interval+loopindex*loopinterval],
            'line':{'color':'FFFF00'},#FF6666
            })       
        
                #所选数据2
           bk_chart.add_series({
            'name':['data', 1, namecol+interval*2+loopindex*loopinterval],
            'categories':['data', data_top, datecol+interval*2+loopindex*loopinterval, data_top+maxlen, datecol+interval*2+loopindex*loopinterval],
            'values':['data', data_top, chgcol+interval*2+loopindex*loopinterval, data_top+maxlen,chgcol+interval*2+loopindex*loopinterval],
            'line':{'color':'336699'},#FF6666
            })  
        
           bk_chart.add_series({
            'name':['data', 1, namecol+interval*3+loopindex*loopinterval],
            'categories':['data', data_top, datecol+interval*3+loopindex*loopinterval, data_top+maxlen, datecol+interval*3+loopindex*loopinterval],
            'values':['data', data_top, chgcol+interval*3+loopindex*loopinterval, data_top+maxlen,chgcol+interval*3+loopindex*loopinterval],
            'line':{'color':'99CC33'},#FF6666
            })    
        
                     
        #   bk_chart.set_title({'name':bktile,
        #                       'name_font': {'size': 10, 'bold': True}
        #                       })
                               
           bk_chart.set_x_axis({'name':u'日期',
                                'name_font': {'size': 10, 'bold': True},
                                'label_position': 'low',
                                'interval_unit': 10                           
                                })
                                
           bk_chart.set_y_axis({'name':'',
                               'name_font': {'size': 10, 'bold': True}
                               })
           
           bk_chart.set_size({'width':width,'height':height})  
         
           return bk_chart  
       
       
        #生成单商品图
        def addChart(loopindex,width,height):
            
           data_top=1
           
           interval=linewidth+1  
           
           bk_chart = wbk.add_chart({'type': 'line'})   
              
           bk_chart.set_style(4)
           
           #向图表添加数据 
           bk_chart.add_series({
            'name':['data', 0, chgcol+loopindex*interval],
            'categories':['data', data_top, datecol+loopindex*interval, data_top+datalen, datecol+loopindex*interval],
            'values':['data', data_top, chgcol+loopindex*interval, data_top+datalen,chgcol+loopindex*interval],
            'line':{'color':'336699'},#FF6666
            })
        
        
        #   bk_chart.add_series({
        #    'name':['data', 0, closecol+loopindex*interval],
        #    'categories':['data', data_top, datecol+loopindex*interval, data_top+datalen, datecol+loopindex*interval],
        #    'values':['data', data_top, closecol+loopindex*interval, data_top+datalen,closecol+loopindex*interval],
        #    'line':{'color':'FF0033'},  
        #    'y2_axis': True,            
        #    })
                     
           bk_chart.set_title({'name':name,
                               #'name_font': {'size': 10, 'bold': True}
                               })
                               
           bk_chart.set_x_axis({#'name':u'日期',
                                #'name_font': {'size': 10, 'bold': True},
                                'label_position': 'low',
                                'interval_unit': 10                           
                                })
                                
        #   bk_chart.set_y_axis({#'name':'',
        #                       'name_font': {'size': 10, 'bold': True}
        #                       })
           
           bk_chart.set_size({'width':width,'height':height})  
         
           return bk_chart 
       
        #计算累计涨幅
        def allChg(df):
            df=df.sort_values('date')
            close0=df['close'].iat[0]
            df['chg']=df['close']/close0-1      
            df['lastchg']=df['chg'].iat[-1]
            return df         
        
        
        if scope == 'industry':
            table = 'industryday'
            #得到商品日线数据
            mdseday=pd.read_sql('select name,industry,date,close from '+table+' where date >= "'+self.sdate+'" and date <= "'+self.edate+'"',con=self.engine)#.drop_duplicates()#board,      
            #得到行业类别
            industries=mdseday['industry'].drop_duplicates()        
            
        else:
            table='boardday'
            #得到商品日线数据
            mdseday=pd.read_sql('select name,board,date,close from '+table+' where date >= "'+self.sdate+'" and date <= "'+self.edate+'"',con=self.engine)#.drop_duplicates()#board,
            #得到板块类别
            industries=mdseday['board'].drop_duplicates() 
            
                 
        mdseday['date']=mdseday['date'].astype(str)  
 
        df_stream=pd.read_sql_table('stream',con=self.engine)
        
        if not os.path.exists(self.fdir):
            os.mkdir(self.fdir)
        
        
        for industry in industries:
            
            fname = self.fdir+industry+'.xlsx'
            
            wbk =xlsxwriter.Workbook(fname) 
            
            picsetsheet=wbk.add_worksheet(u'商品组')
            
            picsheet=wbk.add_worksheet(u'商品及股票')
            
            datasheet=wbk.add_worksheet('data')
            datasheet.hide()
            
            PER=wbk.add_format({'align':'center','valign':'vcenter','font_size':11,'num_format':'0.00%'})
            
            if scope == 'industry':
                df_mdse=mdseday[mdseday.industry==industry]
            
            else:
                df_mdse=mdseday[mdseday.board==industry]
            
            #顶部
            top=0
            
            #左端
            left=0
            
            #数据行宽
            linewidth=6
            
            #数据头
            header=['name','industry','date','close',u'涨幅','lastchg']#,'board'
            
            #获得数据列位置
            datecol=header.index('date')
            
            chgcol=header.index(u'涨幅')
            
            namecol=header.index('name')
            
           # closecol=header.index('close')
    
            df_mdse=df_mdse.groupby('name').apply(allChg)
            
            #按累计涨幅最大排序
            df_mdse.sort_values('lastchg',inplace=True,ascending=False)
            
            #得到最新的，按涨幅排序的商品名
            lastdate=df_mdse['date'].max()
            
            sortnames=df_mdse[df_mdse.date==lastdate]['name'].drop_duplicates()
            
            namenum=len(sortnames)
            
            lenlist=[]
            
            streamleft=19
            streamtop=0
            loop=0
            for name  in sortnames:    
                
                #处理每种商品对应的数据
                data=df_mdse[df_mdse.name==name] 
                datalen=len(data)
                lenlist.append(datalen)
                datasheet.write_row(top,left,header )    
                data.sort_values('date',inplace=True)
                
                #得到每种商品的上下游
                up,down=self.relatedStock(name,df_stream)   
                
                #上下游股票写在图片右边
                picsheet.write(streamtop+2,streamleft,u'上游:')
                picsheet.write_row(streamtop+2,streamleft+1,up)
                
                picsheet.write(streamtop+4,streamleft,u'下游:')
                picsheet.write_row(streamtop+4,streamleft+1,down)                

#                for i in xrange(len(up)):
#                    picsheet.write(streamtop+1+i,streamleft,up.iat[i])
#                    try:
#                        picsheet.write(streamtop+1+i,streamleft+1,down.iat[i])
#                    except:
#                        pass
                
                tmpchart=addChart(loop,1200,600)
                picsheet.insert_chart(streamtop,0,tmpchart)
                    
                for i in xrange(len(data)):        
                    datasheet.write_row(top+i+1,left,data.iloc[i])
                    datasheet.write(top+i+1,left+4,data.iloc[i]['chg'],PER)
                    
                left+=linewidth+1
                streamtop+=30
                loop+=1
            
                
            maxlen=max(lenlist)
            
            lastloopflag=namenum-namenum%4
            
            n=0      
            loop=0    
            left=0        
            while 1:   
                n+=4
                
                if n>lastloopflag:
                    tmpchart=addChartSet(loop,1200,600)
                    picsetsheet.insert_chart(top,left,tmpchart)
                    break
                
                tmpchart=addChartSet(loop,1200,600)    
                picsetsheet.insert_chart(top,left,tmpchart)   
                top+=30      
                loop+=1
            
            wbk.close()
            
            print industry
        

if __name__ == '__main__':
    s=mdsePlot(sdate='2016-08-01',edate='2017-08-23')
    s.plot(scope='industry')