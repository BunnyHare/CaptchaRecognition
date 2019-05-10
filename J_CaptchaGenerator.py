from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import os
import string


def get_content():
    # return random.choice('abcdefghijklmnopqrstuvwxyz0123456789')
    return random.choice('abcdefghkmnopqrstuvwxyz0123456789') # 不生成i j l


def get_background_color():
    return (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))


def get_content_color():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


def make_dir(folder):
    if not os.path.isdir(folder):
        os.makedirs(folder)
    return folder


def generate_random_string(slen=10):
    return ''.join(random.sample(string.ascii_letters + string.digits, slen))


if __name__ == '__main__':
    generate_num = 20  # 要生成的张数
    content_num = 4  # 每张验证码字符个数
    width = 40 * content_num
    height = 60

    path = make_dir('My_captcha4')

    # # 生成训练集（一个图片只有一个小角度旋转的字符）
    # chr_name_list = list('abcdefghijklmnopqrstuvwxyz0123456789')
    # for chr_name in chr_name_list:
    #     sub_path = make_dir(path + '/' + chr_name)
    #     for image_num in range(100):
    #         image = Image.new('RGB', (int(width / content_num), height), (255,255,255))
    #         font = ImageFont.truetype('arial.ttf', 36)
    #         draw = ImageDraw.Draw(image)
    #         # print(chr_name)
    #         # draw.text((10, 10), chr_name, font=font, fill=(0, 0, 0))
    #         image_temp = Image.new('RGB', (int(width / content_num), height), (0, 0, 0))
    #         draw_temp = ImageDraw.Draw(image_temp)
    #         draw_temp.text((10, 10), chr_name, font=font, fill=(255, 255, 255))
    #         image_temp = image_temp.rotate(random.randint(-30, 30))
    #         image.paste(image_temp, (0, 0))
    #         for x in range(int(width / content_num)):
    #             for y in range(height):
    #                 if image.getpixel((x, y)) == (0, 0, 0):
    #                     draw.point((x, y), fill=(255,255,255))
    #                 else:
    #                     draw.point((x, y), fill=(0, 0, 0))
    #         random_suffix_name = generate_random_string()
    #         image.save(sub_path + '/' + chr_name + '_' + random_suffix_name + '.jpg')

    # 生成难以识别的验证码
    for i in range(generate_num):
        image = Image.new('RGB', (width, height), (255, 255, 255))
        font = ImageFont.truetype('arial.ttf', 36)
        draw = ImageDraw.Draw(image)
        random_suffix_name = generate_random_string()
        # 输出文字:
        listChar = []
        for t in range(content_num):
            char = get_content()
            listChar.append(char)

            # # 重叠但不旋转
            # draw.text((random.randint(0, 25) + 40 * t, random.randint(5, 25)), char, fill=get_content_color(),
            #           font=font)

        # 旋转但不重叠
            image_temp = Image.new('RGB', (int(width/content_num), height), (0, 0, 0))
            draw_temp = ImageDraw.Draw(image_temp)
            draw_temp.text((random.randint(5, 15), random.randint(5, 15)), char, fill=get_content_color(), font=font)
            image_temp = image_temp.rotate(random.randint(-30, 30))
            image.paste(image_temp, (40 * t, 0))
        # 填充背景
        for x in range(width):
            for y in range(height):
                if image.getpixel((x, y)) == (0, 0, 0):
                    # draw.point((x, y), fill=(255,255,255))
                    draw.point((x, y), fill=get_background_color())

        image_name = ''.join(listChar)
        image.save(path + '/' + image_name + '_' + random_suffix_name + '.jpg')

    # 验证，提示用户输入一个验证码
    # image.show()
    # user_input = input('请输入验证码:')
    # print(image_name.lower() == user_input.lower())
