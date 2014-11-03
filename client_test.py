# -*- coding: utf-8 -*-
"""
Created on Mon Nov 03 14:11:30 2014

@author: wybert
"""

import suds


url=u'http://localhost:8000/?wsdl'
c=suds.client.Client(url)
#print c

text=u'''最近和初中一同班见面，这家伙当年就极其聪颖，之前在英国拿了物理的学士
加硕士，现在北美攻读理论物理的博士。大致他们学校的教授们还是喜欢用纸笔计算，
所以他们这些学生也还遵循这些传统。当然，计算机的使用是必然的，她写了不少脚
本用于计算实验数据。她很认真地问了我一些关于代码管理之类的问题，在那一刻
我突然想起，自己当初写论文的时候，也有过种种困惑。在过去的三年里，我不光花
了大把时间来写我的博士论文（终于写完了），也花了大把时间来摸索怎样来写作这
么长的论文。之前在豆瓣日志里已经陆续介绍了不少论文写作技术（不是写作技巧）
，现在打算利用专栏的机会系统地介绍这些工具和技巧。'''
top=10
wordfreq_list=c.service.get_word_freq(text,top)

url=c.service.make_word_cloud(wordfreq_list)
print url


