智能服务组合小组webservice
===============================

####使用说明
server.py 提供web服务的服务器
pic_server.py 提供图片服务的http服务器
ciyun.py python代码
client_test.py 客户端测试代码

data文件夹包含用户字典以及停用词以及会生成的图片
pytagclound使用到的包

这个包依赖pygame
注意64位python解释器应安装64位版本的pygame


使用词频服务前应设置用户词典和停用词，最新加入了设置用户字典和停用词的接口，共六个


-----------------------------------------------------------------------------

###分词以及词云图服务webservice

####1. 分词服务

**功能：**把输入的文字进行分词，使用默认的字典以及停用词

**定义：**`def cut_words(text):`

**输入：**

- text：string：需要分词的文本

**输出：**

- word:array: 分得的单词数组



####2. 添加条目到用户字典服务

**功能：**添加一个条目到用户字典

**定义：** `add_item_to_userdict(word,word_freq,word_characteristic)`

**输入：**

- word：string：要添加的词
- word_freq:int: 要添加词的词频
- word_characteristic: 要添加词的词性

**输出：**

- 无


####3. 从用户词典删除一个条目服务

**功能：**从用户词典删除一个条目

**定义：** `delete_item_from_userdict(word)`

**输入：**

- word：string：要删除的词

**输出：**

- 无



####4. 查询用户字典的所有条目服务

**功能：**查询用户字典的所有条目

**定义：** `show_userdict()`

**输入：**

- 无

**输出：**

- 条目列表 每个条目是一个string类型




####5. 添加条目到停用词服务

**功能：**添加一个条目到停用词

**定义：** `add_item_to_stopwords(word)`

**输入：**

- word：string：要添加的词

**输出：**

- 无


####6. 从停用词删除一个条目服务

**功能：**从停用词删除一个条目

**定义：** `delete_item_from_stopwords(word)`

**输入：**

- word：string：要删除的词

**输出：**

- 无



####7. 查询停用词的所有条目服务

**功能：**查询停用词的所有条目

**定义：** `show_stopwords`

**输入：**

- 无

**输出：**

- 条目列表 每个条目是一个string类型



####8. 统计词频服务

**功能：**统计输入文字的词频，使用默认的字典以及停用词返回一个排序好的词频列表（前top个）

**定义：** `def get_word_freq(text,top)`

**输入：**

- text：string：需要统计词频的文本
- top:int: 按词频返回最大的前top个单词的词频

**输出：**

- wordfreq_list:array:词频列表,词频的表示是一个WordFreq抽象数据对象

####9. 生成词云图服务

**功能：**根据一个词频列表，生成一个词语图，返回一个访问该词频图的url

**定义：** `def make_word_cloud(wordfreq_list)`

**输入：**

- wordfreq_list:array:要产生词云图的词频列表,词频的表示是一个WordFreq抽象数据对象

**输出：**

- url:string:词云图的地址


-----------------------------------------------------------

####WordFreq抽象数据类型，包含两个字段

- word=Unicode##词频项
- freq=Integer##词频

**定义如下：**

```python
class WordFreq(ComplexModel):    
    word=Unicode##词频项
    freq=Integer##词频
