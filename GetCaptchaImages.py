import urllib
import urllib.request
import re
import os

def getHtml(url):
    page=urllib.request.urlopen(url)
    html=page.read()
    html=html.decode('utf-8')
    return html

def getImg(html):   # 爬不同网页要修改这里的str
    str = '<img id="loginform-verifycode-image" src="(.*)" alt' # 西电信息化建设处
    imgre=re.compile(str)
    imglist=imgre.findall(html)
    return imglist

def make_dir(folder):
    path=os.getcwd()+'\\'+folder
    if not os.path.isdir(path):
        os.makedirs(path)
    return path

def save_img(url,path,imglist,filename):
    img_url=url+imglist[0]
    img=urllib.request.urlretrieve(img_url,filename)


if __name__=='__main__':
    # '''西电信息化建设处'''
    # path=make_dir('CaptchaImg_xidian')
    # url='https://pay.xidian.edu.cn/'
    # for i in range(5):
    #     html=getHtml(url)
    #     imglist=getImg(html)
    #     filename=path+'\\'+str(i+1)+'.jpg'
    #     print('正在下载第'+str(i+1)+'张图片')
    #     save_img(url,path,imglist,filename)

    # '''饭否'''
    path = make_dir('TrainSet_fanfou')
    download_count=100
    for i in range(download_count):
        filename = path + '\\' + str(i + 1) + '.jpg'
        print('正在下载第' + str(i + 1) + '张图片..')
        urllib.request.urlretrieve('http://captcha.fanfou.com/captcha.png', filename)