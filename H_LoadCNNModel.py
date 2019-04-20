import numpy as np
from keras.models import model_from_json
from G_TrainCNNModel import read_data

if __name__ == '__main__':
    model = model_from_json(open('CNN_model/my_model_architecture.json').read())
    model.load_weights('CNN_model/my_model_weights.h5')

    x_train, x_test, y_train, y_test = read_data()

    # 输出错误的预测结果
    predict_x = model.predict(x_test)
    result = []
    for i in predict_x:
        result.append(np.array(i).argmax())
    result = np.array(result)
    y = []
    for i in y_test:
        y.append(np.array(i).argmax())
    y = np.array(y)
    print('预测错误的序号：')
    for i in range(len(y)):
        if y[i] != result[i]:
            print(i)
