# coding=utf-8
import os
import time
import cv2
import winsound
import pyzbar.pyzbar as pyzbar

waitTime = 3 # 每次掃碼的間隔時間(秒)
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 0  # Set Duration To 1000 ms == 1 second

# winsound.Beep(frequency, duration)
def decode(rawimage, CDtime=0):  #解码
    global barcodeData
    if CDtime <= int(time.time()):
        # 二值化
        if len(rawimage.shape) >= 3:
            image = cv2.cvtColor(rawimage, cv2.COLOR_RGB2GRAY)

        # 获取自适配阈值
        binary, _ = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)

        barcodes = []
        while (binary < 230) and (len(barcodes) == 0):
            binary, mat = cv2.threshold(image, binary, 255, cv2.THRESH_BINARY)
            barcodes = pyzbar.decode(mat)
            binary += 10
        lengthBar = len(barcodes)

        # 有條碼時重置時間
        if lengthBar != 0:
            CDtime = int(time.time()) + waitTime
            
        elif CDtime - int(time.time()) < 0:
            CDtime = int(time.time())
        # elif lengthBar:
        #     return rawimage, CDtime

        for barcode in barcodes:
            # 提取并绘制图像中条形码的边界框
            (x, y, w, h) = barcode.rect
            cv2.rectangle(rawimage, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            # 绘出图像上条形码的数据和条形码类型
            text = "Text:" + barcodeData
            text2 = "Type:" + barcodeType
            font=cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(rawimage,text,(30,30), font, 0.8,(0,255,255),2)
            cv2.putText(rawimage,text2,(30,80), font, 0.8,(0,255,255),2)
            winsound.Beep(frequency, duration)
            Fimg = cv2.resize(rawimage,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_CUBIC)
            # cv2.imshow("result", Fimg)
            # os.system('cls')
            # print(barcodeData)

    # print(CDtime - int(time.time()))
    return rawimage, CDtime

def usecamera():
    global barcodeData
    barcodeData = None
    cdt = int(time.time())
    camera = cv2.VideoCapture(0)
    while True:
        # 读取当前帧
        ret, rawimg = camera.read()
        img, cdt = decode(rawimg, cdt)
            
        #按q键退出程序
        if cv2.waitKey(1) & 0xFF == ord('q'):
            camera.release()
            cv2.destroyAllWindows()  
            break
        if barcodeData != None:
            camera.release()
            cv2.destroyAllWindows()
            return barcodeData


if __name__ == '__main__':
    usecamera()
