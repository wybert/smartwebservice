# -*- coding: utf-8 -*-
"""
Created on Mon Nov 03 11:22:41 2014

@author: wybert
"""

import logging
logging.basicConfig(level=logging.DEBUG)
from spyne.application import Application
from spyne.decorator import rpc
from spyne.service import ServiceBase
from spyne.model.primitive import Integer
from spyne.model.primitive import Unicode
from spyne.model.complex import Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import jieba
import jieba.posseg as pseg
from pytagcloud import create_tag_image, make_tags
from pytagcloud.colors import COLOR_SCHEMES
from spyne.model.complex import ComplexModel








def load_userdict():   
    jieba.load_userdict("data/ap_dict.txt")
    
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



class WordFreq(ComplexModel):    
    word=Unicode
    freq=Integer

class WordFreqAndwordCloudService(ServiceBase):

    @rpc(Unicode,Integer,Unicode) 
    def add_item_to_userdict(ctx,word,word_freq,word_characteristic):
        filehandler=open('data/ap_dict.txt','a')
        filehandler.writelines(word+' '+str(word_freq)+
                        ' '+word_characteristic+'\n')
        filehandler.close()
        
    @rpc(Unicode) 
    def delete_item_from_userdict(ctx,word):    
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
    
    @rpc(_returns=Iterable(Unicode))
    def show_userdict(ctx):
        filehandler=open('data/ap_dict.txt')
        re=[]
        for line in filehandler:
            line=line.strip('\n')
            re+=line
        return re
            
    @rpc(Unicode)
    def add_item_to_stopwords(ctx,word):
        filehandler=open('data/stopwords.txt','a')
        filehandler.writelines(word+'\n')
        filehandler.close()
    
    @rpc(Unicode)
    def delete_item_from_stopwords(ctx,word):    
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
    
    @rpc(_returns=Iterable(Unicode))
    def show_stopwords(ctx):
        filehandler=open('data/stopwords.txt')
        re=[]
        for line in filehandler:
            line=line.strip('\n')
            re+=line
        return re
 
    
    @rpc(Unicode,Integer,_returns=Iterable(WordFreq))           
    def get_word_freq(ctx,text,top):

        STOP_WORD=load_stopword()
        load_userdict()
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
        return_list=[]
        for item in paixu_tiqu:
            wordfreq=WordFreq()
            wordfreq.word=item[0]
            wordfreq.freq=item[1]
            return_list+=[wordfreq]
        return return_list       
    



    @rpc(Iterable(WordFreq),_returns=Unicode)        
    def make_word_cloud(ctx,wordfreq_list):
  
        tupe_list=[]
        for item in wordfreq_list:
            tupe_list+=[(item.word,item.freq)]
        tags = make_tags(dict(tupe_list),maxsize=120,
                         colors=COLOR_SCHEMES['audacity'])
        file_path=u'data/wordfreq.png'
        create_tag_image(tags,file_path, size=(1500, 1200), 
                         fontname='data/simhei.ttf',fontzoom=4)
        url=u'http://localhost:8001/'+file_path
        return url
        
        
application = Application([WordFreqAndwordCloudService],
    tns='spyne.samrtwebservice.wordcloud',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()