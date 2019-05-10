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
import os
import numpy as np


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
    # for i in image_list:
    #     i.show()
    result_arr = []
    for i in range(len(image_list)):
        result_arr.append(recognize_single_character(image_list[i], width, height))
    # for sub_image in image_list:

        # result_arr.append(recognize_single_character(sub_image, width, height))
    result = ''.join(result_arr)
    print('recognize result:'+result)
    return result


if __name__ == '__main__':
    start = time()
    path = os.getcwd() + r'\My_captcha'
    image_count = 0
    correct_count = 0
    for filename in os.listdir(path):
        result = recognize_image(path + '\\' + filename)
        image_count += 1
        answer=filename.split('.')[0].split('_')[0]
        print('answer:'+answer)
        if result == answer:
            correct_count += 1
    print('图片总数：' + str(image_count))
    print('识别正确数：' + str(correct_count))
    print('正确率：' + str(correct_count / image_count))
    # path = 'code.jpg'
    # recognize_image(path)
    print('')
    end = time()
    t = end - start
    print('程序执行时间：' + str(t))
