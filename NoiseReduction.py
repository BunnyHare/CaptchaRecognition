from PIL import Image
import os

def is_black(image,x,y):    #若为黑点，返回1
    if image.getpixel((x,y))==255:
        return 0
    else:
        return 1

def find_nearby_black_pixel(image,x,y,width,height):     # 返回image中坐标为x,y像素周围8个像素的黑色像素数量
    cur_pixel=image.getpixel((x,y))
    if cur_pixel == 255:    # 若为白色不计算
        return 0

    if x==0:    #第一列
        if y==0:    #左上角
            sum=is_black(image,x+1,y)+is_black(image,x,y+1)+is_black(image,x+1,y+1)
            return sum
        elif y==height-1:    #左下角
            sum=is_black(image,x+1,y)+is_black(image,x,y-1)+is_black(image,x+1,y-1)
            return sum
        else:   #最左列中间
            sum=is_black(image,x,y-1)+is_black(image,x+1,y-1)+is_black(image,x+1,y)+is_black(image,x+1,y+1)+is_black(image,x,y+1)
            return sum
    elif x==width-1:    #最后一列
        if y==0:    #右上角
            sum=is_black(image,x-1,y)+is_black(image,x,y+1)+is_black(image,x-1,y+1)
            return sum
        elif y==height-1:    #右下角
            sum=is_black(image,x,y-1)+is_black(image,x-1,y)+is_black(image,x-1,y-1)
            return sum
        else:   #最右列中间
            sum=is_black(image,x,y-1)+is_black(image,x-1,y-1)+is_black(image,x-1,y)+is_black(image,x-1,y+1)+is_black(image,x,y+1)
            return sum
    else:   #除了最左和最右的列
        if y==0:    #第一行
            sum=is_black(image,x-1,y)+is_black(image,x-1,y+1)+is_black(image,x,y+1)+is_black(image,x+1,y+1)+is_black(image,x+1,y)
            return sum
        elif y==height-1:    #最后一行
            sum=is_black(image,x-1,y)+is_black(image,x-1,y-1)+is_black(image,x,y-1)+is_black(image,x+1,y-1)+is_black(image,x+1,y)
            return sum
        else:   #中间
            sum=is_black(image,x-1,y-1)+is_black(image,x,y-1)+is_black(image,x+1,y-1)+\
                is_black(image,x-1,y)+is_black(image,x+1,y)+\
                is_black(image,x-1,y+1)+is_black(image,x,y+1)+is_black(image,x+1,y+1)
            return sum

def noise_reduction(image,threshold):
    width=image.size[0]
    height=image.size[1]
    for x in range(width):
        for y in range(height):
            if find_nearby_black_pixel(image,x,y,width,height)<=threshold:
                image.putpixel((x,y),255)
    return image

if __name__=='__main__':
    path=os.getcwd()+r'\CaptchaTest2'
    noise_reduction_threshold=3     #阈值，周围8个像素黑点数<=阈值认为是噪声
    noise_reduction_again_threshold=2   #再次去噪的阈值，每列每行少于阈值的认为是噪声
    for filename in os.listdir(path):
        if filename.find('_binary')>=0:
            image=Image.open(path+'\\'+filename)
            print('正在对'+filename+'去噪声..')
            image=noise_reduction(image,noise_reduction_threshold)
            image=noise_reduction(image,noise_reduction_threshold)  #两次去噪声，能去除残留的噪点
            new_name=filename.replace('_binary','_noisereduction')
            image.save(path+'\\'+new_name)
