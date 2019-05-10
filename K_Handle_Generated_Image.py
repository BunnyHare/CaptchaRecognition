import os
from PIL import Image
from E_CaptchaSegmentation import segmentation
from I_API import pretreatment, captcha_segmentation

if __name__ == '__main__':
    # 将生成的字符图案分割并归一化，要求传入的图片必须按文件夹分类好
    path = os.getcwd() + '/My_captcha2'
    chr_name_list = list('abcdefghijklmnopqrstuvwxyz0123456789')
    for chr_name in chr_name_list:
        sub_path = path + '/' + chr_name
        for image_name in os.listdir(sub_path):
            image = Image.open(sub_path + '/' + image_name)
            threshold = 3
            width, height = 15, 20
            image = pretreatment(image, threshold)
            image_list = captcha_segmentation(image, width, height)
            for num in range(len(image_list)):
                sub_image_name = image_name
                image_list[num].save(sub_path + '/' + sub_image_name)
