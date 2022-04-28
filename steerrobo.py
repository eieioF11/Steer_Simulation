import sys
import numpy as numpy
from math import radians
from math import degrees
from math import atan2
from math import sin,cos
from math import sqrt
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
from matplotlib.transforms import Affine2D

class steer(object):
    def __init__(self):
        #Parametors--------------------------------------
        figsize=[3,3]#[m]fieldサイズ
        self.size=0.2#[m]robotのbodyサイズ(正方形)
        self.dt=0.01#[s]シュミレーション間隔
        self.wsize_w=0.01#[m]wheel size
        self.wsize_h=0.07#[m]wheel size
        self.wpos=self.size/2#wheel position
        self.r=sqrt(self.wpos**2+self.wpos**2)#[m]
        #------------------------------------------------
        self.fig, self.ax = plt.subplots(1, 1)
        self.ax.set_aspect('equal')
        self.ax.set_xlabel("x[m]")
        self.ax.set_ylabel("y[m]")
        plt.grid()
        self.ax.set_ylim((-figsize[1]/2,figsize[1]/2))
        self.ax.set_xlim((-figsize[0]/2,figsize[0]/2))
        self.fig.canvas.mpl_connect('key_press_event',self.press)
        self.x=0.0
        self.y=0.0
        self.yaw=0.0
        self.vx=0.0
        self.vy=0.0
        self.w=0.0
        self.oldtime=time.time()
        self.wheelangle=[0.0,0.0,0.0,0.0]
        self.key=""
    #キー入力関連
    def press(self,event):
        print('press', event.key)
        sys.stdout.flush()
        self.key=event.key
    def returnkey(self):
        return self.key
    def resetkey(self):
        self.key=""
    #シュミレーション更新
    def update(self):
        nowtime = time.time()
        self.dt=nowtime-self.oldtime
        #座標更新
        self.yaw+=self.w*self.dt
        self.x+=(self.vx*cos(self.yaw)-self.vy*sin(self.yaw))*self.dt
        self.y+=(self.vx*sin(self.yaw)+self.vy*cos(self.yaw))*self.dt
        #ホイール角度計算
        #self.wheelangle[0]=atan2(-self.vx+self.r*self.w*cos(self.yaw),self.vy-self.r*self.w*sin(self.yaw))#A
        #self.wheelangle[1]=atan2(-self.vx+self.r*self.w*sin(self.yaw),self.vy+self.r*self.w*cos(self.yaw))#D
        #self.wheelangle[2]=atan2(-self.vx-self.r*self.w*sin(self.yaw),self.vy-self.r*self.w*cos(self.yaw))#B
        #self.wheelangle[3]=atan2(-self.vx-self.r*self.w*cos(self.yaw),self.vy+self.r*self.w*sin(self.yaw))#C
        self.wheelangle[0]=atan2(-self.vx+self.r*self.w,self.vy-self.r*self.w)#A
        self.wheelangle[1]=atan2(-self.vx+self.r*self.w,self.vy+self.r*self.w)#D
        self.wheelangle[2]=atan2(-self.vx-self.r*self.w,self.vy-self.r*self.w)#B
        self.wheelangle[3]=atan2(-self.vx-self.r*self.w,self.vy+self.r*self.w)#C
        #描画更新
        def relative_rectangle(w: float, h: float, center_tf, **kwargs):
            rect_origin_to_center = Affine2D().translate(w / 2, h / 2)
            return Rectangle(
                (0, 0), w, h, transform=rect_origin_to_center.inverted() + center_tf, **kwargs)

        #body
        to_body_center_tf = Affine2D().rotate(self.yaw).translate(self.x, self.y) + self.ax.transData
        body = relative_rectangle(self.size,self.size, to_body_center_tf, edgecolor='red',fill=False)
        #wheel
        body_center_to_left_front = Affine2D().rotate(self.wheelangle[0]).translate(-self.wpos, self.wpos)
        body_center_to_right_front = Affine2D().rotate(self.wheelangle[1]).translate(self.wpos, self.wpos)
        body_center_to_left_rear = Affine2D().rotate(self.wheelangle[2]).translate(-self.wpos, -self.wpos)
        body_center_to_right_rear = Affine2D().rotate(self.wheelangle[3]).translate(self.wpos, -self.wpos)

        left_front_wheel = relative_rectangle(
            self.wsize_w, self.wsize_h, body_center_to_left_front + to_body_center_tf,
            facecolor='black', edgecolor='black')
        right_front_wheel = relative_rectangle(
            self.wsize_w, self.wsize_h, body_center_to_right_front + to_body_center_tf,
            facecolor='black', edgecolor='black')
        left_rear_wheel = relative_rectangle(
            self.wsize_w, self.wsize_h, body_center_to_left_rear + to_body_center_tf,
            facecolor='black', edgecolor='black')
        right_rear_wheel = relative_rectangle(
            self.wsize_w, self.wsize_h, body_center_to_right_rear + to_body_center_tf,
            facecolor='black', edgecolor='black')
        #追加
        self.ax.add_patch(left_front_wheel)
        self.ax.add_patch(right_front_wheel)
        self.ax.add_patch(left_rear_wheel)
        self.ax.add_patch(right_rear_wheel)
        self.ax.add_patch(body)
        #debag
        print("dt={:6.2f}[s]v({:6.2f},{:6.2f},{:6.2f}),xy({:6.2f},{:6.2f}),yaw={:6.2f},ABCD({:6.2f},{:6.2f},{:6.2f},{:6.2f})".format(self.dt,self.vx,self.vy,self.w,self.x,self.y,degrees(self.yaw),degrees(self.wheelangle[0]),degrees(self.wheelangle[0]),degrees(self.wheelangle[1]),degrees(self.wheelangle[2]),degrees(self.wheelangle[3])))
        #描画
        plt.pause(0.01)
        #削除
        body.remove()
        left_front_wheel.remove()
        right_front_wheel.remove()
        left_rear_wheel.remove()
        right_rear_wheel.remove()
        #時間保存
        self.oldtime=nowtime
    #速度指定
    def move(self,vx,vy,w):
        self.vx=vx
        self.vy=vy
        self.w=w
