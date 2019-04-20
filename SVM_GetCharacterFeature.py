import os
from PIL import Image
from D_NoiseReduction import find_nearby_black_pixel


def getFeature(image):
    # 获取特征值:行和列的黑点数量,比如15*20的图片，前15个是行的黑点数，后20个是列的黑点数，特征向量为35维
    # width, height = image.size # 获取宽和高
    # feature_list = [] # 特征值列表
    # # 每行的特征值
    # for y in range(height):
    #     black_count = 0 # 黑点数量
    #     for x in range(width):
    #         if image.getpixel((x, y)) == 0:  # 黑色
    #             black_count += 1
    #
    #     feature_list.append(black_count)
    #
    # # 每列的特征值
    # for x in range(width):
    #     black_count = 0 # 黑点数量
    #     for y in range(height):
    #         if image.getpixel((x, y)) == 0:  # 黑色
    #             black_count += 1
    #
    #     feature_list.append(black_count)
    #
    # return feature_list

    # 获取特征值，特征值为每个点周围的黑点数
    width, height = image.size  # 获取宽和高
    feature_list = []  # 特征值列表
    for y in range(height):
        for x in range(width):
            feature_list.append(find_nearby_black_pixel(image, x, y, width, height))

    return feature_list


def save_feature(label, feature_list):
    file = open('feature.txt', mode='a')
    # file = open('testfeature.txt', mode='a')
    if label >= 'a' and label <= 'z':
        label = character_to_num(label)
    file.write(label)
    for i in range(len(feature_list)):
        file.writelines(' ' + str(i + 1) + ':' + str(feature_list[i]))
    file.write('\n')
    file.close()


# 用于将a-z转换为10-35
def character_to_num(character):
    if character >= 'a' and character <= 'z':
        character = ord(character) - 87
    return str(character)


if __name__ == '__main__':
    root_path = os.getcwd() + r'\TrainSet'
    # root_path = os.getcwd() + r'\TestSet'
    for root, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            label_folder = root.split('\\')
            label = label_folder[-1]
            image = Image.open(os.path.join(root, filename))
            feature_list = getFeature(image)
            save_feature(label, feature_list)
