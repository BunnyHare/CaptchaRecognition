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
    path=os.getcwd()+r'\TrainSet_fanfou'
    task_path=path+r'\GrayScale'
    save_folder = path+r'\Binaryzation'
    if not os.path.isdir(save_folder):
        os.makedirs(save_folder)
    for filename in os.listdir(task_path):
        if filename.find('_grayscale')>=0:
            image=Image.open(task_path+'\\'+filename)
            print('正在将'+filename+'二值化..')
            image=binaryzation(image)
            bin_filename=filename.replace('_grayscale.jpg','_binary.bmp')
            image.save(save_folder+'\\'+bin_filename)
