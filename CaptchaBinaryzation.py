from PIL import Image
import os

def binaryzation(image):
    threshold=128   # 阈值，在0~255取值，越大越接近白色
    width=image.size[0]
    height=image.size[1]
    image_array=image.load()
    for x in range(width):
        for y in range(height):
            if image_array[x,y]>=threshold:
                image_array[x,y]=255    # 设为白色
            else:
                image_array[x,y]=0      # 设为黑色
    return  image

if __name__=='__main__':
    path=os.getcwd()+r'\CaptchaImg_xidian'
    for filename in os.listdir(path):
        if filename.find('_grayscale')>=0:
            image=Image.open(path+'\\'+filename)
            print('正在将'+filename+'二值化..')
            image=binaryzation(image)
            bin_filename=filename.replace('_grayscale.jpg','_binary.bmp')
            image.save(path+'\\'+bin_filename)
