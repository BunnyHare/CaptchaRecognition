with open(r'H:\Study\CaptchaRecognition\CaptchaImg_fanfou\box\num.font.exp0.box','w') as f:
    # print(f.read())
    for i in range(100):
        f.writelines("A 0 0 15 20 "+str(i)+'\n')
    # print(f.read())