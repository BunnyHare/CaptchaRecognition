from PIL import Image
from A_GetCaptchaImages import make_dir
import os


def grayScale(image):
    image = image.convert('L')  # 调用PIL模块的convert函数，将RGB图片每个像素的分量按照L = R * 299/1000 + G * 587/1000+ B * 114/1000公式转换
    return image


if __name__ == '__main__':
    path = os.getcwd() + r'\TrainSet_fanfou'
    save_folder = path + r'\GrayScale'
    if not os.path.isdir(save_folder):
        os.makedirs(save_folder)
    for fullname in os.listdir(path):
        if fullname.find('.jpg') >= 0:
            print('正在将' + fullname + '灰度化..')
            captcha_img = Image.open(path + '\\' + fullname)
            captcha_img = grayScale(captcha_img)
            new_name = fullname.replace('.jpg', '_grayscale.jpg')
            captcha_img.save(save_folder + '\\' + new_name)
