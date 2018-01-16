import requests
import re
import json
from multiprocessing import Pool
from requests.exceptions import RequestException

def get_one_page(url):
    try:
        response = requests.get(url) #request请求网页
        if response.status_code==200: #判断是否请求成功
            return response.text #成功的话将源代码下载为text
        return None
    except RequestException: #请求异常返回空值
        return None

def parse_one_page(html):
    pattern =  re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'  #（\d+）获取排名，(.*?)获取电影海报地址
                          +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'       #第一个(.*?）获取电影名称，第二个(.*?）获取上映时间
                          +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)      #两个(.*?）分别获取评分的个位和小数位
    item = re.findall(pattern,html)
    for item in item:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4].strip()[5:],
            'star':item[5]+item[6]
        }

def write_to_file(content):
     with open('result.txt', 'a', encoding='utf-8') as f:  #转码输出中文
         f.write(json.dumps(content, ensure_ascii=False) + '\n')
         f.close()

def main(offset):
    url='http://maoyan.com/board/4?offset='+str(offset)#offset表示页数
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__=="__main__" :

    pool=Pool()
    pool.map(main,[i*10 for i in range (10)])#遍历offset实现翻页
