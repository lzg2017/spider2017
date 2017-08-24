# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 16:44:16 2017

@author: Administrator
"""

#coding=utf-8
import urllib
from pyquery import PyQuery as pq
import os


class industryChain:
    
    def __init__(self):
        
        self.picdir=u'E:/股票数据/产业链图/'

    def download(self):
        
        maindoc=pq('http://www.100ppi.com/monitor/')
        
        mainhtml=maindoc.html()
        
        index=maindoc('td[class="stit"]').text().split()
        
        for i in xrange(len(index)):
            
            if i==7:
                usehtml=mainhtml[mainhtml.find('target="_blank">'+index[i]):]
            else:       
                usehtml=mainhtml[mainhtml.find('target="_blank">'+index[i]):mainhtml.find('target="_blank">'+index[i+1])]
            
            usedoc=pq(usehtml)
            
            seconddoc=usedoc('td[class="w1"]')
            
            secondindex=seconddoc.text().split()
            
            for j in xrange(len(secondindex)):
                
                fdir=self.picdir=u'E:/股票数据/产业链图/'+index[i]
                
                if not os.path.exists(fdir):
                    os.mkdir(fdir)
                    
                fname=os.path.join(fdir,secondindex[j]+'.png')
                
                secondurl=seconddoc('a').eq(j).attr.href
                
                thirdhtml=pq('http://www.100ppi.com'+secondurl).html()
                
                pichtml=thirdhtml[thirdhtml.find(u'产业链'):]
                
                picurl=pq(pichtml)('img').attr.src       
        
                urllib.urlretrieve(picurl,fname)
                
                print fname
        

#def getHtml(url):
#    page = urllib.urlopen(url)
#    html = page.read()
#    return html
#
#def getImg(html):
#    reg = r'src="(.+?\.png)" '
#    imgre = re.compile(reg)
    #    imglist = re.findall(imgre,html)
#    x = 0
#    for imgurl in imglist:
#        print imgurl
#        urllib.urlretrieve(imgurl,'%s.png' % x)
#        x+=1
#
#
#html = getHtml("http://www.100ppi.com/price/detail-4218781.html")
#
#getImg(html)