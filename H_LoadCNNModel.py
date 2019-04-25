import numpy as np
from keras.models import model_from_json
from G_TrainCNNModel import read_data
from F_ImageToCsv import image_to_matrix
from PIL import Image
from sklearn.preprocessing import MinMaxScaler


def num_to_character(num):
    if num >= 0 and num <= 9:
        return str(num)
    if num >= 10 and num <= 35:
        return chr(num + 87)


# 识别一张图片
def recognize_image(image, width, height):
    model = model_from_json(open('CNN_model/my_model_architecture.json').read())
    model.load_weights('CNN_model/my_model_weights.h5')
    image_matrix = image_to_matrix(image)
    scale = MinMaxScaler()
    image_matrix = scale.fit_transform(image_matrix)
    image_matrix = image_matrix.reshape(1, width, height, 1)

    predict_val = model.predict(image_matrix)
    predict_array = []
    for i in predict_val:
        predict_array.append(np.array(i).argmax())
    result = num_to_character(predict_array[0])
    return result


if __name__ == '__main__':
    path_x = 'dataset_csv/train_x.csv'
    path_y = 'dataset_csv/train_y.csv'
    model = model_from_json(open('CNN_model/my_model_architecture.json').read())
    model.load_weights('CNN_model/my_model_weights.h5')
    # print(model.summary())
    test_image_path = '1_segmentation_0.bmp'
    test_image = Image.open(test_image_path)
    img_rows, img_cols = test_image.size[0], test_image.size[1]
    test_image_result = recognize_image(test_image, img_rows, img_cols)
    print(test_image_result)

    # 输出错误的预测结果
    x_train, x_test, y_train, y_test = read_data(path_x, path_y)
    predict_x = model.predict(x_test)
    # print(predict_x)
    result = []
    for i in predict_x:
        result.append(np.array(i).argmax())
    result = np.array(result)
    # print(result)
    y = []
    for i in y_test:
        y.append(np.array(i).argmax())
    y = np.array(y)
    print('预测错误的序号：')
    error_count = 0
    for i in range(len(y)):
        if y[i] != result[i]:
            error_count += 1
            print(i)
    print('训练集个数:' + str(len(y)))
    print('识别错误的个数：' + str(error_count))
    print('正确率：' + str(1 - error_count / len(y)))
