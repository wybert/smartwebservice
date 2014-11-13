# -*- coding: utf-8 -*-

import jieba
import jieba.posseg as pseg
from pytagcloud import create_tag_image, make_tags
from pytagcloud.colors import COLOR_SCHEMES
import logging
logging.basicConfig(level=logging.DEBUG)
from spyne.application import Application
from spyne.decorator import rpc
from spyne.service import ServiceBase
from spyne.model.primitive import Integer
from spyne.model.primitive import Float
from spyne.model.primitive import Date,Unicode
from spyne.model.complex import Iterable
#from spyne.protocol.soap import Soap11
#from spyne.server.wsgi import WsgiApplication

#from spyne.model.complex import Array
#import numpy as np
#import cPickle
#import datetime
from spyne.model.complex import ComplexModel


jieba.load_userdict("data/ap_dict.txt")

class WordFreq(ComplexModel):    
    word=Unicode
    freq=Integer

def load_stopword():
    STOP_WORD = set()
    stopword_file = open("data/stopwords.txt")
    for each_line in stopword_file:
        each_line_list = pseg.cut(each_line)
        for elem in each_line_list:
            STOP_WORD.add(elem.word)
        STOP_WORD.add(each_line.strip().decode('utf-8'))
    stopword_file.close()
    return STOP_WORD
# to do  
    
def add_item_to_userdict(word,word_freq,word_characteristic):
    filehandler=open('data/ap_dict.txt','a')
    filehandler.writelines(word+' '+str(word_freq)+
                    ' '+word_characteristic+'\n')
    filehandler.close()
    
def delete_item_from_userdict(word):    
    filehandler=open('data/ap_dict.txt')
    data={}
    for line in filehandler:
        line=line.strip('\n')
        line_list=line.split(' ')
        print line_list[0]
        data[line_list[0]]=line_list[1:]
    filehandler.close()  
    data.pop(word)   
    filehandler=open('data/ap_dict.txt','w')
    for k,v in data.iteritems():
        temp=''    
        for item in v:
            temp+=' '+item
        lines=k+temp+'\n'
        filehandler.writelines(lines)
    filehandler.close()

def show_userdict():
    filehandler=open('data/ap_dict.txt')
    re=[]
    for line in filehandler:
        line=line.strip('\n')
        re+=line
        

def add_item_to_stopwords(word):
    filehandler=open('data/stopwords.txt','a')
    filehandler.writelines(word+'\n')
    filehandler.close()


def delete_item_from_stopwords(word):    
    filehandler=open('data/stopwords.txt')
    data=set()
    for line in filehandler:
        line=line.strip('\n')
        data.add(line)
    filehandler.close()  
    data.discard(word)   
    filehandler=open('data/stopwords.txt','w')
    for item in data:        
        filehandler.writelines(item+'\n')
    filehandler.close()

def show_stopwords():
    filehandler=open('data/stopwords.txt')
    re=[]
    for line in filehandler:
        line=line.strip('\n')
        re+=line
 
      

###########################################################

def get_word_freq(text,top):
    STOP_WORD=load_stopword()
    word_freq = {}
        
    seg_list = pseg.cut(text)
    for ele in seg_list:
        words = ele.word.strip() 
        if ((ele.flag == 'ns' or ele.flag == 'an' 
        or ele.flag == 'nt' or ele.flag == 'nr'
        or ele.flag == 'i'or ele.flag == 'l'
        or ele.flag == 'n') and (words not in STOP_WORD)):
            
            if(word_freq.has_key(words)):
                word_freq[words] += 1
            else:
                word_freq[words] = 1
    paixu= sorted(word_freq.iteritems(), key=lambda d:d[1], reverse = True)
    paixu_tiqu=paixu[0:top]
    re_list=[]
    
    print paixu_tiqu
    for item in paixu_tiqu:
        wordfreq=WordFreq()
        wordfreq.word=item[0]
        wordfreq.freq=item[1]
        re_list+=[wordfreq]
    return re_list

#
#
#raw_file = open("0_all.txt")
#text=u''
#for line in raw_file:
#    text+=line    
#raw_file.close()
#top=10    
#
#
#test=get_word_freq(text,top) 
#
#
#def make_word_cloud(test):
#    paixu_tiqu=[]
#    for item in test:
#        paixu_tiqu+=[(item.word,item.freq)]
#    print paixu_tiqu
#    tags = make_tags(dict(paixu_tiqu),maxsize=120,
#                     colors=COLOR_SCHEMES['audacity'])
#    create_tag_image(tags, 'data/test.png', size=(1500, 1200), 
#                     fontname='simhei.ttf',fontzoom=4)
#    url='test.png'
#    return url
#
#url=make_word_cloud(test)