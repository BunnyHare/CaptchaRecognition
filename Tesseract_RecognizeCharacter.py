from PIL import Image
import pytesseract
import os

def recognizeImage(image):
    # image=Image.open(r'H:\Study\CaptchaRecognition\CaptchaTest2\3_noisereduction.bmp')
    text=pytesseract.image_to_string(image,lang='num', config='--psm 6 --oem 3 tessedit_char_whitelist ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    text = text.lower()
    print(text)
    return text

if __name__=='__main__':
    path=os.getcwd()+r'\RecognizeTest1\新建文件夹'
    file_count=25
    global correct_count
    correct_count=0
    for filename in os.listdir(path):
        image=Image.open(path+'\\'+filename)
        print('正在识别'+filename+'..')
        text=recognizeImage(image)
        if (text+'.bmp')==filename.lower():  # 如果与文件名相同
            correct_count+=1
    correct_rate=correct_count/file_count
    print('正确识别的数量为：' + str(correct_count))
    print('正确率为：'+str(correct_rate))
