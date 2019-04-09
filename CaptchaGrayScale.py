from PIL import Image
import os

def grayScale(image):
    image=image.convert('L')    #调用PIL模块的convert函数，将RGB图片每个像素的分量按照L = R * 299/1000 + G * 587/1000+ B * 114/1000公式转换
    return image

if __name__=='__main__':
    path=os.getcwd()+r'\CaptchaImg_xidian'
    for fullname in os.listdir(path):
        print('正在将' + fullname + '灰度化..')
        (filename,extension)=os.path.splitext(path +'\\' + fullname)
        captcha_img=Image.open(path +'\\' + fullname)
        captcha_img=grayScale(captcha_img)
        captcha_img.save(filename+'_grayscale'+extension)