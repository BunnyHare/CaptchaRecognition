from PIL import Image
import os
import numpy as np
import pandas as pd


def image_to_matrix(image):
    width = image.size[0]
    height = image.size[1]
    image_array = image.load()
    result = []
    for x in range(width):
        temp = []
        for y in range(height):
            temp.append(image_array[x, y])
        result.append(np.array(temp))
    return np.array(result).T


def character_to_num(character):
    if character >= 'a' and character <= 'z':
        character = ord(character) - 87
    return int(character)


def get_data(path):
    all_image_array_x = []
    all_image_array_y = []
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            image = Image.open(os.path.join(root, filename))
            label = root.split('\\')[-1]
            single_image_array_x = image_to_matrix(image)
            if single_image_array_x.shape[0] == 3:
                print(filename)
            all_image_array_x.append(single_image_array_x)
            single_image_array_y = np.zeros(36)
            single_image_array_y[character_to_num(label)] = 1
            all_image_array_y.append(single_image_array_y)
    result_x = all_image_array_x[0]
    for i in range(len(all_image_array_x)-1):
        result_x = np.concatenate((result_x, all_image_array_x[i + 1]))
    # print(result_x.shape)
    # result_x = result_x.reshape(result_x.shape[0] * result_x.shape[1], result_x.shape[2])
    result_y = np.array(all_image_array_y)
    # print(result_y)

    diction_x = {}
    for i in range(result_x.shape[1]):
        diction_x[str(i)] = result_x[:, i]
    result_x = pd.DataFrame(diction_x)
    diction_y = {}
    for i in range(result_y.shape[1]):
        diction_y[str(i)] = result_y[:, i]
    result_y = pd.DataFrame(diction_y)

    print(result_x)
    # print(result_y)

    result_x.to_csv('dataset_csv/train_x.csv', index=False)
    result_y.to_csv('dataset_csv/train_y.csv', index=False)


if __name__ == '__main__':
    path = os.getcwd() + r'\My_captcha2'
    get_data(path)
