import A_GetCaptchaImages
import B_CaptchaGrayScale
import C_CaptchaBinaryzation
import D_NoiseReduction
import E_CaptchaSegmentation
import H_LoadCNNModel
import urllib
import urllib.request
import sys
from PIL import Image
from time import time


def get_captcha_images(download_count):
    # '''西电信息化建设处'''
    path = A_GetCaptchaImages.make_dir('CaptchaImg_xidian')
    url = 'https://pay.xidian.edu.cn/'
    for i in range(download_count):
        html = A_GetCaptchaImages.getHtml(url)
        imglist = A_GetCaptchaImages.getImg(html)
        filename = path + '\\' + str(i + 1) + '.jpg'
        print('正在下载第' + str(i + 1) + '张图片')
        A_GetCaptchaImages.save_img(url, path, imglist, filename)

    # '''饭否'''
    path = A_GetCaptchaImages.make_dir('TrainSet_fanfou')
    for i in range(download_count):
        filename = path + '\\' + str(i + 1) + '.jpg'
        print('正在下载第' + str(i + 1) + '张图片..')
        urllib.request.urlretrieve('http://captcha.fanfou.com/captcha.png', filename)


def captcha_grayscale(image):
    return B_CaptchaGrayScale.grayScale(image)


def captcha_binaryzation(image):
    return C_CaptchaBinaryzation.binaryzation(image)


def captcha_noise_reduction(image, threshold):
    if threshold > 8 or threshold < 0:
        print('阈值必须在0到8之间')
        sys.exit()
    return D_NoiseReduction.noise_reduction(image, threshold)


def pretreatment(image, threshold):
    image = captcha_grayscale(image)
    image = captcha_binaryzation(image)
    image = captcha_noise_reduction(image, threshold)
    # image.show()
    return image


def captcha_segmentation(image, resize_width, resize_height):
    image_list = E_CaptchaSegmentation.segmentation(image, resize_width, resize_height)
    return image_list


def recognize_single_character(image, width, height):
    image_result = H_LoadCNNModel.recognize_image(image, width, height)
    return image_result


def recognize_image(image_path):
    image = Image.open(image_path)
    threshold = 3
    width, height = 15, 20
    image = pretreatment(image, threshold)
    image_list = captcha_segmentation(image, width, height)
    result = []
    for sub_image in image_list:
        result.append(recognize_single_character(sub_image, width, height))

    for i in result:
        print(i, end='')


if __name__ == '__main__':
    start = time()
    path = '14.jpg'
    recognize_image(path)
    print('')
    end = time()
    t = end - start
    print('程序执行时间：'+str(t))
