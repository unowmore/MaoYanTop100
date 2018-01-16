import requests
import re
import json
from multiprocessing import Pool
from requests.exceptions import RequestException

def get_one_page(url):
    try:
        response = requests.get(url) #request������ҳ
        if response.status_code==200: #�ж��Ƿ�����ɹ�
            return response.text #�ɹ��Ļ���Դ��������Ϊtext
        return None
    except RequestException: #�����쳣���ؿ�ֵ
        return None

def parse_one_page(html):
    pattern =  re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'  #��\d+����ȡ������(.*?)��ȡ��Ӱ������ַ
                          +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'       #��һ��(.*?����ȡ��Ӱ���ƣ��ڶ���(.*?����ȡ��ӳʱ��
                          +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)      #����(.*?���ֱ��ȡ���ֵĸ�λ��С��λ
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
     with open('result.txt', 'a', encoding='utf-8') as f:  #ת���������
         f.write(json.dumps(content, ensure_ascii=False) + '\n')
         f.close()

def main(offset):
    url='http://maoyan.com/board/4?offset='+str(offset)#offset��ʾҳ��
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__=="__main__" :

    pool=Pool()
    pool.map(main,[i*10 for i in range (10)])#����offsetʵ�ַ�ҳ
