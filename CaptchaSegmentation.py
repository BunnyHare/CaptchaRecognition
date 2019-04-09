from PIL import Image
import os

def vertical_segmentation(image):
    width=image.size[0]
    height=image.size[1]
    sub_image_list=[]
    left=-1  # 子图左边界的坐标
    white_column_flag=False    # 判断整列是否都是白色的标志
    connect_threshold=20    # 粘连阈值，认为如果一个子图片的宽度像素超过阈值说明可能是两个字符粘连在一起了

    for x in range(width):
        for y in range(height):     # 纵向遍历
            if image.getpixel((x,y))==0:    # 如果遇到黑点
                if left==-1:    # 如果还没到左边界，说明现在是左边界
                    left=x
                    white_column_flag=False
                    break
                else:   # 过了左边界（但可能是中间也可能是右边界）
                    white_column_flag=False
                    break
            white_column_flag=True

        if white_column_flag==True and left!=-1:    # 整列都是白色且已经找到了左边界，说明处于右边界
            sub_image=image.crop((left,0,x,height))
            if x-left>connect_threshold:    # 子图是两个字符粘连在一起的情况，需要再次分割
                min_black_pixel_count=height
                segment_position=0
                for sub_x in range(5,sub_image.width):
                    current_column_black_pixel=0
                    for sub_y in range(height):
                        if sub_image.getpixel((sub_x,sub_y))==0:
                            current_column_black_pixel+=1
                    if current_column_black_pixel<min_black_pixel_count:
                        min_black_pixel_count=current_column_black_pixel
                        segment_position=sub_x
                sub_image_segment1=sub_image.crop((0,0,segment_position,height))
                sub_image_segment2=sub_image.crop((segment_position+1,0,sub_image.width,height))
                sub_image_list.append(sub_image_segment1)
                sub_image_list.append(sub_image_segment2)
            else:
                sub_image_list.append(sub_image)
            left=-1

    return sub_image_list

def horizontal_segmentation(image):
    width=image.size[0]
    height=image.size[1]
    top=-1
    white_row_flag=False
    for y in range(height):
        for x in range(width):     # 纵向遍历
            if image.getpixel((x,y))==0:    # 如果遇到黑点
                if top==-1:    # 如果还没到上边界，说明现在是上边界
                    top=y
                    white_row_flag=False
                    break
                else:   # 过了上边界（但可能是中间也可能是下边界）
                    white_row_flag=False
                    break
            white_row_flag=True
        if white_row_flag==True and top!=-1:
            global sub_image
            sub_image=image.crop((0,top,width,y))
            break
    return sub_image

def segmentation(image,resize_width,resize_height):
    image_list=vertical_segmentation(image)
    for i in range(len(image_list)):
        image_list[i]=horizontal_segmentation(image_list[i])
        image_list[i]=image_list[i].resize((resize_width, resize_height),Image.ANTIALIAS)   # 重新调整大小
    return image_list

if __name__=='__main__':
    path=os.getcwd()+r'\CaptchaImg_fanfou'
    image_list=[]
    resize_width=15
    resize_height=20
    for filename in os.listdir(path):
        if filename.find('_noisereduction')>=0:
            image=Image.open(path+'\\'+filename)
            print('正在分割'+filename+'..')
            image_list=segmentation(image,resize_width,resize_height)
            for num in range(len(image_list)):
                sub_image_name=filename.replace('_noisereduction.bmp','_segmentation_' + str(num)+'.bmp')
                image_list[num].save(path+'\\'+sub_image_name)
