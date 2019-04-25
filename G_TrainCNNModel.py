import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.layers import Conv2D
from sklearn.preprocessing import MinMaxScaler

batch_size = 128  # 批处理样本数量
nb_classes = 36  # 分类数目
epochs = 600  # 迭代次数
img_count = 1020  # 图片数量
img_rows, img_cols = 15, 20  # 输入图片样本的宽高
nb_filters = 32  # 卷积核的个数
pool_size = (2, 2)  # 池化层的大小
kernel_size = (3, 3)  # 卷积核的大小
input_shape = (img_rows, img_cols, 1)  # 输入图片的维度


def read_data(path_x,path_y):
    x = pd.read_csv(path_x).values
    scale = MinMaxScaler()
    x = scale.fit_transform(x)
    y = pd.read_csv(path_y).values
    x = x.reshape(img_count, img_rows, img_cols, 1)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)
    return x_train, x_test, y_train, y_test


def get_model():
    model = Sequential()
    model.add(Conv2D(6, kernel_size, input_shape=input_shape, strides=1))  # 卷积层
    model.add(Flatten())  # 拉成一维数据
    model.add(Dense(nb_classes))  # 全连接层
    model.add(Activation('softmax'))
    return model


if __name__ == '__main__':
    path_x='dataset_csv/train_x.csv'
    path_y='dataset_csv/train_y.csv'
    x_train, x_test, y_train, y_test = read_data(path_x,path_y)
    model = get_model()
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    # 训练模型
    model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=2, validation_data=(x_test, y_test))

    # 保存模型
    json_string = model.to_json()
    open('CNN_model/my_model_architecture.json', 'w').write(json_string)
    model.save_weights('CNN_model/my_model_weights.h5')
