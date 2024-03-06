import mediapipe as mp
import math
import numpy as np
import time
import cv2
# from flask import  Blueprint
# from flask import Flask, render_template, Response
from application.utils.camera import cap
# from flask import Flask, request


class gesTure:
#初始化
    def __init__(self):
        self.mphands = mp.solutions.hands #mediapipe手部关键点检测的方法
        self.hands = self.mphands.Hands(min_detection_confidence=0.75,min_tracking_confidence=0.75)
        self.mpDraw = mp.solutions.drawing_utils #绘制手部关键点的连线的方法
        self.pointStyle = self.mpDraw.DrawingSpec(color=(255, 0, 255), thickness=4)  # 点的样式
        self.lineStyle = self.mpDraw.DrawingSpec(color=(0, 0, 255), thickness=4)  # 线的样式

#主函数
    def Control(self):
        print(1)
        camera1 = cv2.VideoCapture(0)

        self.plocx,self.plocy,self.smooth = 0,0,6  #上一帧时的鼠标所在位置,自定义平滑系数，让鼠标移动平缓一些
        self.resize_w,self.resize_h= 640,480 # 原窗口大小
        self.pt1,self.pt2 = (50,50),(600,300) # 虚拟鼠标的移动范围，左上坐标pt1，右下坐标pt2
        self.pTime = 0  # 设置第一帧开始处理的起始时间

        while cap.video.isOpened():
            red,self.img = cap.video.read()
            if red:
                self.img = cv2.flip(self.img, 1)  # 镜头翻转
                self.GesTure_control()

                cv2.rectangle(self.img,self.pt1,self.pt2,(138,12,92),3) #弄一个框
                self.Frame_Rate()
                ret, buffer = cv2.imencode('.jpg', self.img)
                # 将缓存里的流数据转成字节流
                frame = buffer.tobytes()
                # 指定字节流类型image/jpeg
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            if cv2.waitKey(1) == 27: #ESC退出
                break


        # while 1:
        #     red, self.img = camera1.read()
        #     if red:
        #         frame = cv2.flip(frame,1)
        #         ret1,buffer = cv2.imencode('.jpg',frame)
        #         #将缓存里的流数据转成字节流
        #         frame = buffer.tobytes()
        #         #指定字节流类型image/jpeg
        #         yield  (b'--frame\r\n'
        #                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        #
        #         # self.img = cv2.flip(self.img, 1)  # 镜头翻转
                # self.GesTure_control()
                #
                # cv2.rectangle(self.img, self.pt1, self.pt2, (138, 12, 92), 3)  # 弄一个框
                # self.Frame_Rate()
                # ret, buffer = cv2.imencode('.jpg', self.img)
                # # 将缓存里的流数据转成字节流
                # frame = buffer.tobytes()
                # # 指定字节流类型image/jpeg
                # yield (b'--frame\r\n'
                #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            # if cv2.waitKey(1) == 27:  # ESC退出
            #     break
        #手势识别
    def GesTure_control(self):
        imgRGB = cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB) #把BGR转换为RGB
        result = self.hands.process(imgRGB)
        if result.multi_hand_landmarks: #判断是否检测到手
            for self.handLms in result.multi_hand_landmarks: # 获得手的坐标，线，画出来
                self.mpDraw.draw_landmarks(self.img,self.handLms,self.mphands.HAND_CONNECTIONS, self.pointStyle, self.lineStyle) #把关键点连起来
                self.Count()

#计算关键点的距离(有_的是用来获取坐标的，没有_的是用来距离比较的)
    def Count(self):
        #0到食指关节
        p0x = self.handLms.landmark[0].x
        p0y = self.handLms.landmark[0].y
        p5x = self.handLms.landmark[5].x
        p5y = self.handLms.landmark[5].y
        distance_0_5 = pow(p0x - p5x, 2) + pow(p0y - p5y, 2)
        self.dis05 = pow(distance_0_5, 0.5) #0到5的距离

        #拇指坐标
        p4x = self.handLms.landmark[4].x
        p4y = self.handLms.landmark[4].y
        p4_x = math.ceil(p4x * self.resize_w)
        p4_y = math.ceil(p4y * self.resize_h)
        self.thumb = (p4_x,p4_y)
        distance_4_5 = pow(p4x - p5x, 2) + pow(p4y - p5y, 2)
        self.dis45 = pow(distance_4_5, 0.5) #拇指到5的距离

        #食指坐标
        p8x = self.handLms.landmark[8].x
        p8y = self.handLms.landmark[8].y
        self.p8_x = math.ceil(self.handLms.landmark[8].x * self.resize_w)
        self.p8_y = math.ceil(self.handLms.landmark[8].y * self.resize_h)
        self.index = (self.p8_x,self.p8_y)
        distance_0_8 = pow(p0x - p8x, 2) + pow(p0y - p8y, 2)
        self.dis08 = pow(distance_0_8, 0.5) #0到食指的距离

        #中指坐标
        p12x = self.handLms.landmark[12].x
        p12y = self.handLms.landmark[12].y
        self.p12_x = math.ceil(self.handLms.landmark[12].x * self.resize_w)
        self.p12_y = math.ceil(self.handLms.landmark[12].y * self.resize_h)
        self.middle = (self.p12_x,self.p12_y)
        distance_0_12 = pow(p0x-p12x,2) + pow(p0y-p12y,2)
        self.dis012 = pow(distance_0_12,0.5) #0到中指的距离
        distance_8_12 = pow(p8x - p12x,2) + pow(p8y - p12y,2)
        self.dis812 = pow(distance_8_12,0.5)

        #无名指坐标
        p16x = self.handLms.landmark[16].x
        p16y = self.handLms.landmark[16].y
        self.p16_x = math.ceil(self.handLms.landmark[16].x * self.resize_w)
        self.p16_y = math.ceil(self.handLms.landmark[16].y * self.resize_h)
        self.ring = (self.p16_x,self.p16_y)
        distance_0_16 = pow(p0x-p16x,2) + pow(p0y-p16y,2)
        self.dis016 = pow(distance_0_16,0.5) #无名指到0的距离

        #尾指的坐标
        p20x = self.handLms.landmark[20].x
        p20y = self.handLms.landmark[20].y
        self.p20_x = math.ceil(self.handLms.landmark[20].x * self.resize_w)
        self.p20_y = math.ceil(self.handLms.landmark[20].y * self.resize_h)
        self.caudal = (self.p20_x,self.p20_y)
        distance_0_20 = pow(p0x-p20x,2) + pow(p0y-p20y,2)
        self.dis020 = pow(distance_0_20,0.5) #尾指到0的位置
        distance_16_20 = pow(p16x-p20x,2) + pow(p16y-p20y,2)
        self.dis1620 = pow(distance_16_20,0.5) #16到20的距离
        print(self.dis1620)

        self.img = cv2.circle(self.img, self.index, 10, (255, 0, 0), cv2.FILLED) #食指的样式
        self.img = cv2.circle(self.img, self.thumb, 10 ,(255, 0, 0), cv2.FILLED) #拇指样式
        self.img = cv2.circle(self.img, self.middle, 10, (255, 0, 0), cv2.FILLED) #中指样式
        self.img = cv2.circle(self.img, self.ring, 10, (0, 255, 0), cv2.FILLED) #无名指的样式
        self.img = cv2.circle(self.img, self.caudal, 10, (0, 255, 0), cv2.FILLED) #尾指的样式
        self.EXEcute_judge()


#判断手势
    def EXEcute_judge(self):
#手势指令
        #关灯
        if self.dis45 < 0.02:
            print(2)
            # # 将处理结果写入"text2"文件
            # with open("/downloads/text2", "w") as file:
            #     file.write('2')

        # 开灯
        elif self.dis012 < self.dis05 and self.dis08 > self.dis05*1.4 and self.dis812 > 0.07:
            print(1)
            # # 将处理结果写入"text2"文件
            # with open("/downloads/text2", "w") as file:
            #     file.write('1')
        else:
            print(0)
            # # 将处理结果写入"text2"文件
            # with open("/downloads/text2", "w") as file:
            #     file.write('0')

#显示FPS
    def Frame_Rate(self):
        self.cTime = time.time()  # 处理完一帧图像的时间
        self.fps = 1 / (self.cTime - self.pTime)
        self.pTime = self.cTime #重置起始时间
        cv2.putText(self.img,str(int(self.fps)),(70,40),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
#
# gesture_bp = Blueprint('gesture', __name__, url_prefix='/gesture')
# ges = gesTure()

# def gen(ges, cap):
#     while True:
#         frame = ges.Control(cap)
#         # 使用 generator 函数输出视频流， 每次请求输出的 content 类型是 image/jpeg
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#
# @gesture_bp.route('/ges_video')  # 这个地址返回视频流响应
# def gesture():
#     return Response(gen(ges, cap),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# x = gesTure()
# x.Control(cap)