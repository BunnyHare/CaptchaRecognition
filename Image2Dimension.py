from PIL import Image
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D
from keras.models import model_from_json
from sklearn.preprocessing import MinMaxScaler

batch_size = 128  # 批处理样本数量
nb_classes = 36  # 分类数目
epochs = 600  # 迭代次数
img_rows, img_cols = 20, 15  # 输入图片样本的宽高
nb_filters = 32  # 卷积核的个数
pool_size = (2, 2)  # 池化层的大小
kernel_size = (3, 3)  # 卷积核的大小
input_shape = (img_rows, img_cols, 1)  # 输入图片的维度


def ImageToMatrix(image):
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


def get_data():
    path = os.getcwd() + r'\TrainSet'
    all_image_array_x = []
    all_image_array_y = []
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            image = Image.open(os.path.join(root, filename))
            label = root.split('\\')[-1]
            single_image_array_x = ImageToMatrix(image)
            all_image_array_x.append(single_image_array_x)
            single_image_array_y = np.zeros(36)
            single_image_array_y[character_to_num(label)] = 1
            # print(single_image_array_y)
            all_image_array_y.append(single_image_array_y)
    result_x = np.array(all_image_array_x)
    result_x = result_x.reshape(result_x.shape[0] * result_x.shape[1], result_x.shape[2])
    # print(result_x)
    result_y = np.array(all_image_array_y)
    # print(result_y)

    # diction_x = {str(i): result_x[:, i] for i in range(result_x.shape[1])}
    diction_x = {}
    for i in range(result_x.shape[1]):
        diction_x[str(i)] = result_x[:, i]
    result_x = pd.DataFrame(diction_x)
    # diction_y = {str(i): result_y[:, i] for i in range(result_y.shape[1])}
    diction_y = {}
    for i in range(result_y.shape[1]):
        diction_y[str(i)] = result_y[:, i]
    result_y = pd.DataFrame(diction_y)

    result_x.to_csv('dataset_csv/train_x.csv', index=False)
    result_y.to_csv('dataset_csv/train_y.csv', index=False)


def get_model():
    model = Sequential()
    model.add(Conv2D(6, kernel_size, input_shape=input_shape, strides=1))  # 卷积层1
    model.add(Flatten())  # 拉成一维数据
    model.add(Dense(36))  # 全连接层2
    model.add(Activation('softmax'))
    return model


if __name__ == '__main__':
    get_data()
    x = pd.read_csv('dataset_csv/train_x.csv').values
    scale = MinMaxScaler()
    x = scale.fit_transform(x)
    y = pd.read_csv('dataset_csv/train_y.csv').values
    x = x.reshape(1020, 20, 15, 1)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)
    model = get_model()
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    # 训练模型
    # model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=2, validation_data=(x_test, y_test))
    #
    # score = model.evaluate(x_test, y_test)
    # print('score:', score)

    # 输出错误的预测结果
    # pre = model.predict(x_test)
    # result = []
    # for i in pre:
    #     result.append(np.array(i).argmax())
    # result = np.array(result)
    # y = []
    # for i in y_test:
    #     y.append(np.array(i).argmax())
    # y = np.array(y)
    # for i in range(len(y)):
    #     if y[i] != result[i]:
    #         print(i)

    # save architecture
    json_string = model.to_json()
    open('./my_model_architecture.json', 'w').write(json_string)
    # save weights
    model.save_weights('./my_model_weights.h5')

    # 加载模型
    my_model = model_from_json(open('./my_model_architecture.json').read())
    my_model.load_weights('./my_model_weights.h5')
    # print(my_model.summary())
    # num_x = x_test.shape[0]
    print(y_test[0:2])
    print(my_model.predict(x_test[0:2]))

