import requests
from bs4 import BeautifulSoup
import re
import os

def requestWeb(webUrl):  # url由其他方法传入
    
    # 请求的首部信息
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/65.0.3325.146 Safari/537.36 '
    }
    # 利用requests对象的get方法，对指定的url发起请求
    # 该方法会返回一个Response对象
    res = requests.get(webUrl, headers=headers)
    # 解决中文乱码
    res.encoding = res.apparent_encoding
    # 通过Response对象的text方法获取网页的文本信息
    html = res.text
    # 初始化html页面
    beautifulSoup = BeautifulSoup(html, 'lxml')
    return beautifulSoup

def getVideoUrl(soup):
    urlGroup = re.search(r"http(.*?)mp4", soup)
    if urlGroup != None:
        return urlGroup.group(0)
    else:
        return False

def getTitle(soup):
    return soup.select("h1 a")[0].text + soup.select("h1 span")[0].text
    

if __name__ == '__main__':
    while(True):
        aUrl = input('请输入樱花动漫具体动漫的网址（键入-1退出）：')
        if aUrl == '-1':
            break
        videoCode = re.search(r"\d+", aUrl).group(0)
        print('视频编号：' + videoCode)
        title = requestWeb('http://www.yhdm.io/show/' + str(videoCode) + '.html').select("h1")[0].text
        print('动漫标题：' + title)
        with open(os.path.join(os.getcwd(), title + '.dpl'), 'w', encoding="utf-8") as file:
            file.write('DAUMPLAYLIST\nplayname=\ntopindex=0\n\n')
            for i in range(5000):
                soup = requestWeb('http://www.yhdm.io/v/' + str(videoCode) + '-' + str(i+1) +'.html')
                videoUrl = getVideoUrl(str(soup))
                if  videoUrl != False:
                    file.write(str(i+1) + '*file*' + videoUrl + '\n' + str(i+1) + '*title*' + str(getTitle(soup)) + '\n' + str(i+1) + '*played*0\n\n')
                    print('写入' + str(getTitle(soup)) + '链接为：' + videoUrl)
                else:
                    print(title + '.dpl已生成，敬请享用吧！')
                    break
