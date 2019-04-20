from svmutil import *

def trainSvmModel():
    # 读取特征值文件
    y, x = svm_read_problem('svm_feature/feature.txt')

    #训练得到模型F
    model = svm_train(y, x, '-q')# 静默模式

    # 保存模型
    svm_save_model('svm_feature/feature_model', model)

    return model # 返回模型

if __name__ == '__main__':
    yt, xt = svm_read_problem('svm_feature/testfeature.txt')
    # model = trainSvmModel()
    model=svm_load_model('svm_feature/feature_model')
    print('测试:')
    p_label, p_acc, p_val = svm_predict(yt, xt, model)
    print("结果:\n", p_label)